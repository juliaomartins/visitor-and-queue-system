# Assistant Memory, Chat History and Languages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The dashboard assistant saves every conversation in PostgreSQL per admin, remembers within a conversation and (on request) across conversations, and answers as a specialist in English, European Portuguese and Tetun.

**Architecture:** `apps/assistant` gains its first models (`Conversation`, `ChatMessage`, `MemoryNote`) and three focused modules: `services.py` (persistence), `memory.py` (gated notes), `languages.py` (glossary + rules). The chat route stops taking a transcript from the browser and loads history from the database; new routes list, open and delete conversations and notes. The popup gains a History view.

**Tech Stack:** Django 6.1 + DRF, LangChain 1.5 `create_agent`, langchain-openai, Next.js 16 + TanStack Query, generated `@vms/contracts`.

**Spec:** `docs/superpowers/specs/2026-11-13-assistant-memory-design.md`

## Global Constraints

- Run Python as `..\.venv\Scripts\python.exe` from `vms-backend/`. Tests: `..\.venv\Scripts\python.exe manage.py test apps.assistant --settings=config.settings.test`.
- Never run uvicorn; the owner restarts it by hand. Never touch the live Postgres — tests use `config.settings.test` (SQLite) only.
- No test calls OpenAI: pass a fake model (`GenericFakeChatModel` subclass whose `bind_tools` returns `self`) to `agent.ask(model=...)`, or patch `apps.assistant.agent._model`.
- After any serializer change: `./scripts/check_contracts.sh` from the repo root (Git Bash), then stage the three generated files. Never hand-edit `vms-contracts/src/schema.d.ts`.
- Locale codes are exactly `en`, `pt`, `tet` (the dashboard's `Locale` type).
- Dashboard strings go through `vms-dashboard/scripts/generate-locales.py` (run with the venv Python); never edit `lib/locales/*.ts` by hand.
- Nothing from a conversation goes in `localStorage`/`sessionStorage`.
- Data tools stay read-only. The only writing tool is `remember`, and it exists only when the admin's own message asks to remember.
- Work on branch `feature/assistant-memory`, never on `main`.

## Review Focus

- **Another admin's conversation id** (guessed or copied URL) → 404 on open, delete and chat, never the content. Test in Task 3.
- **A visitor name carrying "remember: …"** reaches the model through a tool result while the admin never said remember → no `remember` tool exists that turn. Test in Task 2.
- **OpenAI fails mid-question** → nothing saved; retrying the same text saves exactly one question and one answer. Test in Task 3.
- **A purged visitor's name in an old transcript** → replaced by `[deleted visitor]`, case-insensitively. Test in Task 1.
- **A conversation longer than 20 messages** → only the last 20 are sent to the model, oldest first. Test in Task 1.

---

### Task 1: Models, persistence services, test settings, purge redaction

**Files:**
- Create: `vms-backend/config/settings/test.py`
- Create: `vms-backend/apps/assistant/models.py`
- Create: `vms-backend/apps/assistant/migrations/__init__.py`, `0001_initial.py` (generated)
- Create: `vms-backend/apps/assistant/services.py`
- Create: `vms-backend/apps/assistant/tests/__init__.py`, `tests/factories.py`, `tests/test_services.py`
- Modify: `vms-backend/apps/visitors/services.py` (`purge_visitor`)

**Interfaces:**
- Produces (models, `apps/assistant/models.py`):
  - `Conversation(BaseModel)`: `owner` FK `settings.AUTH_USER_MODEL` CASCADE `related_name="assistant_conversations"`; `title` CharField(120, blank); `locale` CharField(8, choices `Locale` = en/pt/tet, default `"en"`). `Meta.ordering = ("-updated_at",)`, index on `("owner", "-updated_at")`.
  - `ChatMessage(TimeStampedModel)`: `id` BigAutoField; `conversation` FK CASCADE `related_name="messages"`; `role` CharField(10, choices user/assistant); `content` TextField; `downloads` JSONField(default=list, blank=True); `tools_used` JSONField(default=list, blank=True). `Meta.ordering = ("id",)`.
  - `MemoryNote(BaseModel)`: `owner` FK CASCADE `related_name="assistant_memories"`; `text` CharField(200). `Meta.ordering = ("created_at",)`.
- Produces (`apps/assistant/services.py`):
  - `HISTORY_LIMIT = 20`, `TITLE_CHARS = 80`, `REDACTED = "[deleted visitor]"`
  - `get_owned(owner, conversation_id) -> Conversation` — raises `Conversation.DoesNotExist` unless owned.
  - `history(conversation: Conversation | None) -> list[dict]` — last `HISTORY_LIMIT` messages as `{"role", "content"}`, oldest first; `[]` for `None`.
  - `record_exchange(owner, conversation: Conversation | None, *, question: str, locale: str, result: dict) -> tuple[Conversation, ChatMessage, ChatMessage]` — atomic; creates the conversation when `None`; title = first line of the first question, cut to `TITLE_CHARS` with `…`; bumps `updated_at`. `result` is `agent.ask`'s dict (`answer`, `downloads`, `tools_used`).
  - `redact_visitor(full_name: str) -> int` — case-insensitive replace in `ChatMessage.content`; returns rows changed; no-op for names under 3 characters.

- [ ] **Step 1: Write `config/settings/test.py`** — `from .dev import *`; SQLite `NAME = BASE_DIR / "test.sqlite3"`; `OPENAI_API_KEY = ""`; `PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]`; `MEDIA_ROOT` under a temp dir. Add `test.sqlite3` to `vms-backend/.gitignore` if not ignored.

- [ ] **Step 2: Write the failing tests** in `tests/test_services.py` (factories: `make_admin(username)`, `make_visitor(full_name, country="Timor-Leste")` with unique serial/hash):

```python
def test_record_exchange_creates_conversation_and_both_messages(self):
    conv, q, a = services.record_exchange(admin, None, question="How many arrived?\nmore", locale="pt",
        result={"answer": "**3**", "downloads": [OFFER], "tools_used": ["entrance_report"]})
    assert conv.owner == admin and conv.locale == "pt" and conv.title == "How many arrived?"
    assert [m.role for m in conv.messages.all()] == ["user", "assistant"]
    assert a.downloads == [OFFER] and a.tools_used == ["entrance_report"]

def test_title_is_cut_to_80_chars_with_ellipsis(self): ...  # len == 80, endswith "…"
def test_second_exchange_keeps_title_and_bumps_updated_at(self): ...
def test_history_returns_last_20_oldest_first(self):  # 25 exchanges -> 50 msgs
    h = services.history(conv)
    assert len(h) == 20 and h[0]["content"] == "q15" and h[-1]["content"] == "a24"
def test_history_of_none_is_empty(self): assert services.history(None) == []
def test_get_owned_refuses_other_admins_conversation(self):
    with self.assertRaises(Conversation.DoesNotExist): services.get_owned(other, conv.id)
def test_purge_visitor_redacts_name_in_transcripts(self):
    # message "Ana Maria Sousa arrived; ANA MARIA SOUSA again" -> both replaced by REDACTED
    purge_visitor(visitor)
    assert "ana maria sousa" not in msg_refreshed.content.lower() and msg_refreshed.content.count(REDACTED) == 2
def test_redact_ignores_names_under_3_chars(self): assert services.redact_visitor("Al") == 0
```

- [ ] **Step 3: Run to verify they fail** — Run the test command. Expected: errors importing `apps.assistant.models` / `services`.

- [ ] **Step 4: Implement the models, run `manage.py makemigrations assistant --settings=config.settings.test`, implement `services.py`, and call `redact_visitor(visitor.full_name)` inside `purge_visitor` before `visitor.delete()`** (import inside the function — `assistant` depends on `visitors`, not the reverse at import time).

- [ ] **Step 5: Run to verify they pass** — Expected: all `test_services` tests OK. Also `manage.py makemigrations --check --dry-run` → "No changes detected".

- [ ] **Step 6: Commit** — `git commit -m "Save assistant conversations per admin; redact purged visitors from them"`

---

### Task 2: Languages, gated memory, agent wiring

**Files:**
- Create: `vms-backend/apps/assistant/languages.py`, `vms-backend/apps/assistant/memory.py`
- Modify: `vms-backend/apps/assistant/tools.py` (`Session`, `build_tools`), `vms-backend/apps/assistant/agent.py` (`SYSTEM_PROMPT`, `ask`)
- Test: `vms-backend/apps/assistant/tests/test_languages.py`, `tests/test_memory.py`, `tests/test_agent.py`

**Interfaces:**
- Consumes: `MemoryNote` (Task 1).
- Produces (`languages.py`):
  - `SPECIALIST = ("en", "pt", "tet")`
  - `GLOSSARY: tuple[tuple[str, str, str], ...]` — (English, European Portuguese, Tetun). Must include at least: visitor/visitante/vizitante; registered/inscrito/rejistadu; arrived/chegou/to'o; arrival/chegada/xegada; badge/crachá/kartaun; refused at the door/recusado à entrada/rejeita iha odamatan; door/porta/odamatan; entrance report/relatório de entradas/relatóriu tama; day/dia/loron; people/pessoas/ema; country/país/nasaun; organisation/organização/organizasaun; valid/válido/válidu; duplicate/duplicado/duplikadu; revoked/revogado/revogadu; deactivated badge/crachá desativado/kartaun desativadu; download/descarregar/deskarega; Excel workbook/livro Excel/livru Excel. Tetun and Portuguese spellings match `vms-dashboard/scripts/generate-locales.py` where the term exists there.
  - `language_guide(interface_locale: str) -> str` — the prompt section: answer in the language of the user's latest message; specialist rules for the three (European Portuguese: registo/ecrã/telemóvel, never "você"/"registro"/"tela"; Tetun Dili, INL orthography, no Portuguese sentences inside a Tetun answer, count people as "ema na'in N"); any other language answered competently with the same figures; dd/mm/yyyy and 24-hour time everywhere; the glossary as `en | pt | tet` lines; when the message is too short to tell, use `interface_locale` (unknown codes fall back to `en`), named by its language name.
- Produces (`memory.py`):
  - `MAX_NOTES = 20`, `MAX_NOTE_CHARS = 200`
  - `class MemoryRefused(Exception)` — `str(e)` is a sentence the model can relay.
  - `wants_memory(text: str) -> bool` — case-insensitive word match on: remember, memorise/memorize, don't forget, lembr*, memoriz*, hanoin, keta haluha.
  - `notes_for(owner) -> list[MemoryNote]`
  - `save_note(owner, text: str) -> MemoryNote` — strips; refuses empty, > `MAX_NOTE_CHARS`, at `MAX_NOTES`, or containing any `Visitor.full_name` (≥ 4 chars, case-insensitive, deleted rows included); an existing note with the same text (iexact) is returned, not duplicated.
  - `memory_section(notes: list[MemoryNote]) -> str` — `""` when empty; otherwise a prompt block of the notes as `- text` lines, framed as the admin's preferences.
- Produces (`tools.py`): `Session` gains `remembered: list[str]`; `build_tools(session, *, owner=None, allow_memory: bool = False)` adds a `remember(note: str)` tool only when `allow_memory and owner is not None`; it calls `memory.save_note`, appends to `session.remembered`, and returns either a confirmation or the refusal sentence.
- Produces (`agent.py`): `ask(messages: list[dict], *, actor, locale: str = "en", model=None) -> dict` — loads `memory.notes_for(actor)`, sets `allow_memory = memory.wants_memory(messages[-1]["content"])`, appends `language_guide(locale)` and `memory_section(...)` to the system prompt (replacing the old one-line "answer in the language the user writes in" style rule), and returns `{"answer", "downloads", "tools_used", "remembered"}`.

- [ ] **Step 1: Write the failing tests**

```python
# test_languages.py
def test_guide_names_interface_language_and_falls_back(self):
    assert "Tetun" in language_guide("tet") and "English" in language_guide("xx")
def test_guide_carries_every_glossary_row(self):
    g = language_guide("en"); assert all(f"{en} | {pt} | {tet}" in g for en, pt, tet in GLOSSARY)
def test_glossary_has_required_terms(self):
    assert {"visitor", "badge", "refused at the door", "entrance report"} <= {r[0] for r in GLOSSARY}

# test_memory.py
@parameterized: "Remember that Gate B is the side gate", "lembra-te disto", "Favor hanoin ida ne'e", "keta haluha" -> True
                "How many arrived?", "who is a member?" -> False
def test_save_note_refuses_visitor_name(self):  # visitor "Ana Maria Sousa"; note "ana maria sousa is VIP" -> MemoryRefused
def test_save_note_refuses_over_200_chars_and_21st_note(self): ...
def test_save_note_deduplicates_case_insensitively(self): assert MemoryNote.objects.count() == 1
def test_memory_section_empty_and_listed(self): assert memory_section([]) == "" and "- Answer in Tetun" in memory_section([n])

# test_agent.py  (FakeToolModel scripted with AIMessages)
def test_remember_tool_absent_unless_admin_asks(self):
    # admin message "How many arrived?"; fake model calls `remember` -> tool not found; no MemoryNote saved
def test_remember_tool_saves_when_admin_asks(self):
    out = agent.ask([{"role": "user", "content": "Remember: answer in Tetun"}], actor=admin, model=fake_calling_remember("Answer in Tetun"))
    assert out["remembered"] == ["Answer in Tetun"] and MemoryNote.objects.filter(owner=admin).count() == 1
def test_saved_notes_and_language_guide_reach_system_prompt(self):
    # capture the messages the fake model receives; system text contains "- Answer in Tetun" and "Tetun Dili"
def test_ask_still_scrubs_invented_links(self): ...  # sandbox link removed (existing behaviour kept)
```

- [ ] **Step 2: Run to verify they fail** — Expected: ImportError on `languages` / `memory`; agent tests fail on missing `remembered`.

- [ ] **Step 3: Implement `languages.py`, `memory.py`, then the `tools.py` and `agent.py` changes** per the Interfaces block. Keep `_scrub`, the author rule and every existing prompt rule.

- [ ] **Step 4: Run to verify they pass** — Expected: all assistant tests OK.

- [ ] **Step 5: Commit** — `git commit -m "Teach the assistant three languages and to remember on request"`

---

### Task 3: API — chat on stored history, conversations and memories routes

**Files:**
- Modify: `vms-backend/apps/assistant/serializers.py`, `views.py`, `urls.py`
- Regenerate: `vms-backend/openapi.yaml`, `vms-contracts/openapi.yaml`, `vms-contracts/src/schema.d.ts`
- Test: `vms-backend/apps/assistant/tests/test_api.py`

**Interfaces:**
- Consumes: `services.*` (Task 1), `agent.ask(..., locale=)` returning `remembered` (Task 2).
- Produces (HTTP, all `IsAdmin`; `Conversation` ids are UUIDs):
  - `POST /api/v1/assistant/chat` (throttle scope `assistant`) — request `{conversation?: uuid|null, message: str (1–4000, trimmed), locale?: "en"|"pt"|"tet" = "en"}` → 200 `{conversation: ConversationSummary, question: ChatMessage, answer: ChatMessage, remembered: string[]}`; 404 for a conversation not owned; existing 502/503 mapping unchanged, and on any failure nothing is saved.
  - `GET /api/v1/assistant/conversations` → `ConversationSummary[]` (own, newest first, at most 50): `{id, title, locale, created_at, updated_at, message_count}`.
  - `GET /api/v1/assistant/conversations/{id}` → `ConversationSummary & {messages: ChatMessage[]}`; 404 if not owned.
  - `DELETE /api/v1/assistant/conversations/{id}` → 204; 404 if not owned.
  - `GET /api/v1/assistant/memories` → `{id, text, created_at}[]`; `DELETE /api/v1/assistant/memories/{id}` → 204; 404 if not owned.
  - `ChatMessage` = `{id: int, role, content, downloads: DownloadOffer[], created_at}`.
  - Schema component names: `ConversationSummary`, `ConversationDetail`, `ChatMessage`, `ChatRequest`, `ChatResponse`, `MemoryNote` (reuse `DownloadOffer`).
  - `GET /api/v1/assistant/status` unchanged.

- [ ] **Step 1: Write the failing tests** (`APIClient.force_authenticate`; patch `apps.assistant.agent._model` with a fake):

```python
def test_chat_without_conversation_creates_one_and_saves_both_messages(self):
    r = post({"message": "How many arrived?", "locale": "tet"})
    assert r.status_code == 200 and r.json()["conversation"]["locale"] == "tet"
    assert ChatMessage.objects.count() == 2
def test_followup_sends_stored_history_to_model(self):  # capture fake model input: contains the first question text
def test_chat_on_other_admins_conversation_is_404_and_saves_nothing(self): ...
def test_failed_answer_saves_nothing_and_retry_saves_once(self):
    # first fake raises openai.APIConnectionError -> 503, 0 messages; retry same text -> 200, exactly 2 messages
def test_list_is_own_only_newest_first_with_counts(self): ...
def test_detail_and_delete_are_404_for_other_admin(self): ...
def test_delete_removes_conversation_and_messages(self): ...
def test_memories_list_and_delete_own_only(self): ...
def test_message_over_4000_chars_and_blank_message_are_400(self): ...
def test_non_staff_is_403(self): ...
```

- [ ] **Step 2: Run to verify they fail** — Expected: 400/404 mismatches against the old `messages[]` contract.

- [ ] **Step 3: Implement serializers, views (`ConversationListView`, `ConversationDetailView` with `get` + `delete`, `MemoryListView`, `MemoryDetailView` `delete`; `AssistantChatView` calls `services.get_owned` → `services.history` + new message → `agent.ask(locale=)` → `services.record_exchange`) and routes.** `message_count` via `Count("messages")` annotation. Keep the error handling in `AssistantChatView` as it is.

- [ ] **Step 4: Run to verify they pass** — Expected: all assistant tests OK; `manage.py check` clean.

- [ ] **Step 5: Regenerate contracts** — Run `./scripts/check_contracts.sh` from the repo root; stage the three generated files; re-run → "contracts are up to date".

- [ ] **Step 6: Commit** — `git commit -m "Serve assistant chat from stored history; add conversation and memory routes"`

---

### Task 4: Dashboard — history, memories, locale

**Files:**
- Modify: `vms-dashboard/lib/assistant.ts`, `vms-dashboard/components/assistant/AssistantDock.tsx`, `vms-dashboard/app/globals.css`, `vms-dashboard/scripts/generate-locales.py` (+ regenerated `lib/locales/*.ts`)
- Create: `vms-dashboard/components/assistant/HistoryView.tsx`

**Interfaces:**
- Consumes: the HTTP contract of Task 3 through `@vms/contracts`.
- Produces (`lib/assistant.ts`): `useConversations(enabled: boolean)`, `useConversation(id: string | null)`, `useMemories(enabled: boolean)`, `askAssistant(input: {conversation: string | null; message: string; locale: Locale}): Promise<ChatResponse>`, `deleteConversation(id: string)`, `deleteMemory(id: string)`. Query keys: `["assistant","conversations"]`, `["assistant","conversation",id]`, `["assistant","memories"]`. `MAX_HISTORY` and client-side transcript slicing are removed.
- Produces (`HistoryView.tsx`): `HistoryView({ activeId, onOpen, onBack }: { activeId: string | null; onOpen(id: string): void; onBack(): void })` — conversation rows (title or "Untitled", relative time from `useFormat().relative`), two-step delete (Delete → Confirm), then a "Remembered" section with each note and a Forget button, and the hint that saying "remember…" adds one.
- Panel behaviour: header buttons History, New conversation, Close. `activeId` in React state only. Messages shown = `useConversation(activeId)` messages + a pending user bubble while asking. On success: `setActiveId(reply.conversation.id)`, append `question` and `answer` into the conversation cache, invalidate the list (and memories when `remembered.length`). A non-empty `remembered` shows "Remembered: …" under that answer. Retry re-sends the pending text. Empty state keeps the suggestions and adds up to three recent conversations. `locale` from `useLocale()`.
- New message keys (en / pt / tet, generator): `assistant.history`, `assistant.newConversation`, `assistant.historyTitle`, `assistant.historyEmpty`, `assistant.recent`, `assistant.untitled`, `assistant.deleteConversation`, `assistant.confirmDelete`, `assistant.memoriesTitle`, `assistant.memoriesHint`, `assistant.memoriesEmpty`, `assistant.forget`, `assistant.remembered` (`"Remembered: {note}"`), `assistant.loadFailed`, `assistant.backToChat`. Remove `assistant.clear`.

- [ ] **Step 1: Add the keys to the generator and regenerate** — Expected: generator prints three files, non-ascii=0, equal key counts.
- [ ] **Step 2: Implement `lib/assistant.ts`, `HistoryView.tsx`, the panel changes and styles** (component classes in `globals.css`, unlayered, like the existing `.assistant-*`).
- [ ] **Step 3: Verify** — Run `npx tsc --noEmit -p .`, `npx eslint components/assistant lib/assistant.ts`, `npm test`. Expected: no output from tsc/eslint; tests 0 fail.
- [ ] **Step 4: Visual check** — throwaway harness at `app/(public)/desk/zz-assistant-preview/` with canned responses (pattern from the previous session): chat with a stored conversation, History view with notes, light and dark, 1440 and 390 wide; delete the harness after.
- [ ] **Step 5: Commit** — `git commit -m "Show assistant history and memories in the panel"`

---

### Task 5: Documentation and final verification

**Files:**
- Modify: `CLAUDE.md` (assistant section: models now exist — "NO MODELS" line in Backend structure, "Stateless" bullet; chat history contains visitor names and is redacted on purge; memory gate; languages; test command; build table), `vms-backend/.gitignore` if needed.

- [ ] **Step 1: Update CLAUDE.md** so every claim about the assistant matches the code.
- [ ] **Step 2: Full verification** — assistant tests, `manage.py check`, `makemigrations --check --dry-run`, `check_contracts.sh`, dashboard tsc/eslint/test. Expected: all clean.
- [ ] **Step 3: Live smoke test** against the throwaway SQLite probe DB with the real key: a Tetun question, a Portuguese question, "remember: answer briefly" then a new conversation honouring it.
- [ ] **Step 4: Commit** — `git commit -m "Document assistant memory, history and languages"`
