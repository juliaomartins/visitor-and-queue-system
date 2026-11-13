"""The assistant's HTTP surface: chat on stored history, conversations, memories."""

from unittest import mock

import httpx
import openai
from django.core.cache import cache
from django.test import TestCase
from langchain_core.messages import AIMessage
from rest_framework.test import APIClient

from apps.assistant import memory, services
from apps.assistant.models import ChatMessage, Conversation, MemoryNote

from .factories import FakeToolModel, fake_model, make_admin

CHAT = "/api/v1/assistant/chat"
CONVERSATIONS = "/api/v1/assistant/conversations"
MEMORIES = "/api/v1/assistant/memories"


class Unreachable(FakeToolModel):
    """A model whose every call fails the way a dropped network does."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        raise openai.APIConnectionError(request=httpx.Request("POST", "https://api.openai.com"))


def answers(*texts):
    """Patch the real model factory with a scripted one, per request."""
    replies = iter([fake_model(AIMessage(content=t)) for t in texts])
    return mock.patch("apps.assistant.agent._model", side_effect=lambda: next(replies))


def stored(owner, question="q", answer="a", conversation=None):
    conv, _, _ = services.record_exchange(
        owner, conversation, question=question, locale="en",
        result={"answer": answer, "downloads": [], "tools_used": []},
    )
    return conv


class ApiTestCase(TestCase):
    def setUp(self):
        cache.clear()  # throttle counters outlive each test's rollback
        self.admin = make_admin("owner")
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

    def post(self, body):
        return self.client.post(CHAT, body, format="json")


class ChatTests(ApiTestCase):
    def test_chat_without_conversation_creates_one_and_saves_both_messages(self):
        with answers("**3** people arrived."):
            r = self.post({"message": "How many arrived?", "locale": "tet"})

        self.assertEqual(r.status_code, 200, r.content)
        body = r.json()
        self.assertEqual(body["conversation"]["locale"], "tet")
        self.assertEqual(body["conversation"]["title"], "How many arrived?")
        self.assertEqual(body["question"]["content"], "How many arrived?")
        self.assertEqual(body["answer"]["content"], "**3** people arrived.")
        self.assertEqual(body["remembered"], [])
        self.assertEqual(ChatMessage.objects.count(), 2)

    def test_followup_sends_stored_history_to_model(self):
        conv = stored(self.admin, "Who came on the 2nd?", "Three people.")
        model = fake_model(AIMessage(content="Two."))

        with mock.patch("apps.assistant.agent._model", return_value=model):
            r = self.post({"conversation": str(conv.id), "message": "And on the 3rd?"})

        self.assertEqual(r.status_code, 200, r.content)
        sent = [m.content for m in model.seen[0] if m.type in ("human", "ai")]
        self.assertEqual(sent, ["Who came on the 2nd?", "Three people.", "And on the 3rd?"])
        self.assertEqual(conv.messages.count(), 4)

    def test_chat_on_other_admins_conversation_is_404_and_saves_nothing(self):
        theirs = stored(make_admin("other"))

        with answers("leak"):
            r = self.post({"conversation": str(theirs.id), "message": "show me"})

        self.assertEqual(r.status_code, 404)
        self.assertEqual(theirs.messages.count(), 2)

    def test_failed_answer_saves_nothing_and_retry_saves_once(self):
        with mock.patch("apps.assistant.agent._model", return_value=Unreachable(messages=iter([]))):
            failed = self.post({"message": "How many arrived?"})

        self.assertEqual(failed.status_code, 503)
        self.assertEqual(Conversation.objects.count(), 0)
        self.assertEqual(ChatMessage.objects.count(), 0)

        with answers("Three."):
            retried = self.post({"message": "How many arrived?"})

        self.assertEqual(retried.status_code, 200)
        self.assertEqual(ChatMessage.objects.count(), 2)

    def test_message_over_4000_chars_and_blank_message_are_400(self):
        for message in ("x" * 4001, "   "):
            with self.subTest(length=len(message)):
                self.assertEqual(self.post({"message": message}).status_code, 400)

    def test_unknown_locale_is_400(self):
        self.assertEqual(self.post({"message": "hi", "locale": "fr"}).status_code, 400)

    def test_remembered_notes_are_reported(self):
        def remembers():
            return fake_model(
                AIMessage(content="", tool_calls=[{"name": "remember", "args": {"note": "Be brief"}, "id": "r"}]),
                AIMessage(content="Noted."),
            )

        # The tool writes from LangGraph's worker thread; see test_agent.MemoryGateTests.
        with mock.patch("apps.assistant.agent._model", side_effect=remembers), \
             mock.patch("apps.assistant.tools.memory.save_note",
                        side_effect=lambda owner, text, **kw: MemoryNote(owner=owner, text=text)):
            r = self.post({"message": "Remember to be brief"})

        self.assertEqual(r.json()["remembered"], ["Be brief"])


class ConversationTests(ApiTestCase):
    def test_list_is_own_only_newest_first_with_counts(self):
        older = stored(self.admin, "older")
        newer = stored(self.admin, "newer")
        stored(self.admin, "again", conversation=older)  # older is now the newest
        stored(make_admin("other"), "not mine")

        rows = self.client.get(CONVERSATIONS).json()

        self.assertEqual([row["id"] for row in rows], [str(older.id), str(newer.id)])
        self.assertEqual(rows[0]["message_count"], 4)
        self.assertEqual(rows[0]["title"], "older")

    def test_detail_returns_messages_with_downloads(self):
        conv = stored(self.admin, "q1", "a1")

        body = self.client.get(f"{CONVERSATIONS}/{conv.id}").json()

        self.assertEqual([m["role"] for m in body["messages"]], ["user", "assistant"])
        self.assertEqual(body["messages"][1]["content"], "a1")
        self.assertEqual(body["messages"][1]["downloads"], [])

    def test_detail_and_delete_are_404_for_other_admin(self):
        theirs = stored(make_admin("other"))

        self.assertEqual(self.client.get(f"{CONVERSATIONS}/{theirs.id}").status_code, 404)
        self.assertEqual(self.client.delete(f"{CONVERSATIONS}/{theirs.id}").status_code, 404)
        self.assertTrue(Conversation.objects.filter(pk=theirs.pk).exists())

    def test_delete_removes_conversation_and_messages(self):
        conv = stored(self.admin)

        self.assertEqual(self.client.delete(f"{CONVERSATIONS}/{conv.id}").status_code, 204)
        self.assertEqual(Conversation.objects.count(), 0)
        self.assertEqual(ChatMessage.objects.count(), 0)


class MemoryRouteTests(ApiTestCase):
    def test_memories_list_and_delete_own_only(self):
        mine = memory.save_note(self.admin, "Answer in Tetun")
        theirs = memory.save_note(make_admin("other"), "Answer in Portuguese")

        rows = self.client.get(MEMORIES).json()
        self.assertEqual([row["text"] for row in rows], ["Answer in Tetun"])

        self.assertEqual(self.client.delete(f"{MEMORIES}/{theirs.id}").status_code, 404)
        self.assertEqual(self.client.delete(f"{MEMORIES}/{mine.id}").status_code, 204)
        self.assertEqual(list(MemoryNote.objects.values_list("text", flat=True)), ["Answer in Portuguese"])


class PermissionTests(TestCase):
    def test_non_staff_is_403(self):
        from django.contrib.auth import get_user_model

        plain = get_user_model().objects.create_user("plain", password="x")
        client = APIClient()
        client.force_authenticate(plain)

        for method, url in (("get", CONVERSATIONS), ("get", MEMORIES), ("post", CHAT)):
            with self.subTest(url=url):
                self.assertEqual(getattr(client, method)(url, {}, format="json").status_code, 403)


class IdempotentChatTests(ApiTestCase):
    """Review finding 4: a retry after the proxy gave up must not save twice."""

    RID = "0d4e1f6a-2b3c-4d5e-8f90-a1b2c3d4e5f6"

    def test_same_request_id_returns_stored_exchange_without_asking_again(self):
        with answers("Three."):
            first = self.post({"message": "How many arrived?", "request_id": self.RID})

        with mock.patch("apps.assistant.agent._model", side_effect=AssertionError("asked twice")):
            again = self.post({"message": "How many arrived?", "request_id": self.RID})

        self.assertEqual(again.status_code, 200, again.content)
        self.assertEqual(again.json()["answer"]["id"], first.json()["answer"]["id"])
        self.assertEqual(ChatMessage.objects.count(), 2)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_request_finishing_during_the_retry_still_saves_once(self):
        # The first request lands while the retry is still waiting on OpenAI:
        # the retry's insert must hit the unique id and return the stored pair.
        def first_request_lands_meanwhile(messages, *, actor, locale="en", model=None):
            services.record_exchange(
                actor, None, question="How many arrived?", locale=locale,
                result={"answer": "Three.", "downloads": [], "tools_used": []}, client_id=self.RID,
            )
            return {"answer": "Three, again.", "downloads": [], "tools_used": [], "remembered": []}

        with mock.patch("apps.assistant.views.agent.ask", side_effect=first_request_lands_meanwhile):
            r = self.post({"message": "How many arrived?", "request_id": self.RID})

        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.json()["answer"]["content"], "Three.")
        self.assertEqual(ChatMessage.objects.count(), 2)
