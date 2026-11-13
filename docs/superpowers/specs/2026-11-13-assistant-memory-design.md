# Assistant memory, chat history and languages — design

**Date:** 2026-11-13 · **Status:** decided by Claude on the owner's instruction
("whatever you do — do it as the best code"), open to correction.

## Intent

The dashboard's data assistant (`apps/assistant`, the popup) forgets everything:
the conversation is React state, gone on reload, and nothing is kept. The owner
wants it to **remember**, to **save every chat in the database**, and to be a
**specialist in English, Portuguese and Tetun** while answering any other
language competently.

## Decisions

1. **Chat history lives in PostgreSQL, private per admin.** A `Conversation`
   belongs to one admin; its `ChatMessage` rows hold every question and answer,
   with the offered downloads and the tools used. An admin sees, reopens and
   deletes only their own conversations. No sharing between admins.
2. **Memory inside a conversation is server-side.** The server loads the last
   20 messages of the conversation from the database and sends them to the
   model; the dashboard sends only the new message. A reload no longer loses
   anything.
3. **Memory across conversations is explicit notes.** When — and only when —
   the admin's own latest message asks to remember something ("remember…",
   "lembra…", "hanoin…", "keta haluha…"), the model gets a `remember` tool. A
   note is ≤200 characters, an admin keeps ≤20, and every note is shown in the
   panel with a Forget button. Notes are injected into every future
   conversation of that admin.
   - **Why gated:** tool results contain visitor names typed by the public. A
     memory that any text could create would be a *persistent* prompt
     injection. Gating on the admin's own words closes that.
   - **No visitor data in notes:** a note containing any registered visitor's
     full name is refused. Notes are for preferences and terminology ("answer
     in Tetun", "Gate B means the side gate"), not facts about people — facts
     about people go stale and are re-retrieved every time anyway.
4. **Languages.** English, European Portuguese and Tetun Dili are the
   specialist languages: one shared glossary of the event's terms (taken from
   the dashboard's own translations where they exist), European Portuguese
   (registo, ecrã, telemóvel — never Brazilian), Tetun in the INL orthography
   with loanwords spelled the Tetun way, dd/mm/yyyy and 24-hour times in all
   three. Any other language: answer in that language, same figures, no
   glossary. The dashboard's interface language is sent as a hint and decides
   only when the message itself is too short to tell (a name, "ok", a number).
5. **Privacy follow-through.** Transcripts quote visitor names. Permanently
   deleting a visitor (`purge_visitor`) replaces their full name in every saved
   message with `[deleted visitor]`, or "erase for good" would leave them in
   chat history.
6. **A failed answer saves nothing.** The question and the answer are written
   together after the model succeeds; a failure leaves the database untouched
   and the dashboard offers Retry with the same text — so a retry never
   duplicates a question.
7. **Real tests.** `config/settings/test.py` (SQLite), as CLAUDE.md prescribes
   for the first real suite; `manage.py test apps.assistant
   --settings=config.settings.test`. No OpenAI call in any test.

## Non-goals

- Sharing conversations between admins; exporting chat history.
- Streaming answers.
- Automatic summaries of past conversations as memory (stale figures,
  visitor data, cost).
- A better model for Tetun: the key reaches `gpt-4o-mini` only. The glossary and
  rules are what can be improved without one.

## Constraints

Hard constraints in CLAUDE.md all hold: one process, no Redis/Celery, read-only
data tools, `schema.d.ts` regenerated not edited, nothing visitor-related in
`localStorage`.
