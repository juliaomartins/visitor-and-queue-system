"""Conversation persistence, and what a purge must take out of it."""

from django.test import TestCase

from apps.assistant import services
from apps.assistant.models import ChatMessage, Conversation
from apps.visitors.services import purge_visitor

from .factories import make_admin, make_visitor

OFFER = {
    "report": "entrance_report",
    "format": "xlsx",
    "filters": {
        "date_from": "2026-10-02",
        "date_to": "2026-10-02",
        "country": None,
        "category": None,
        "result": None,
    },
}


def reply(answer: str = "ok", downloads=None, tools=None) -> dict:
    return {"answer": answer, "downloads": downloads or [], "tools_used": tools or []}


class RecordExchangeTests(TestCase):
    def setUp(self):
        self.admin = make_admin()

    def test_record_exchange_creates_conversation_and_both_messages(self):
        conv, question, answer = services.record_exchange(
            self.admin,
            None,
            question="How many arrived?\nand more detail",
            locale="pt",
            result=reply("**3**", [OFFER], ["entrance_report"]),
        )

        self.assertEqual(conv.owner, self.admin)
        self.assertEqual(conv.locale, "pt")
        self.assertEqual(conv.title, "How many arrived?")
        self.assertEqual([m.role for m in conv.messages.all()], ["user", "assistant"])
        self.assertEqual(question.content, "How many arrived?\nand more detail")
        self.assertEqual(answer.content, "**3**")
        self.assertEqual(answer.downloads, [OFFER])
        self.assertEqual(answer.tools_used, ["entrance_report"])

    def test_title_is_cut_to_80_chars_with_ellipsis(self):
        conv, _, _ = services.record_exchange(
            self.admin, None, question="x" * 200, locale="en", result=reply()
        )

        self.assertEqual(len(conv.title), services.TITLE_CHARS)
        self.assertTrue(conv.title.endswith("…"))

    def test_second_exchange_keeps_title_and_bumps_updated_at(self):
        conv, _, _ = services.record_exchange(
            self.admin, None, question="First", locale="en", result=reply()
        )
        before = conv.updated_at

        again, _, _ = services.record_exchange(
            self.admin, conv, question="Second", locale="en", result=reply()
        )

        again.refresh_from_db()
        self.assertEqual(again.pk, conv.pk)
        self.assertEqual(again.title, "First")
        self.assertGreater(again.updated_at, before)
        self.assertEqual(again.messages.count(), 4)


class HistoryTests(TestCase):
    def setUp(self):
        self.admin = make_admin()

    def test_history_returns_last_20_oldest_first(self):
        conv = None
        for n in range(25):
            conv, _, _ = services.record_exchange(
                self.admin, conv, question=f"q{n}", locale="en", result=reply(f"a{n}")
            )

        history = services.history(conv)

        self.assertEqual(len(history), services.HISTORY_LIMIT)
        self.assertEqual(history[0], {"role": "user", "content": "q15"})
        self.assertEqual(history[-1], {"role": "assistant", "content": "a24"})

    def test_history_of_none_is_empty(self):
        self.assertEqual(services.history(None), [])


class OwnershipTests(TestCase):
    def test_get_owned_refuses_other_admins_conversation(self):
        owner, other = make_admin("owner"), make_admin("other")
        conv, _, _ = services.record_exchange(
            owner, None, question="mine", locale="en", result=reply()
        )

        self.assertEqual(services.get_owned(owner, conv.id), conv)
        with self.assertRaises(Conversation.DoesNotExist):
            services.get_owned(other, conv.id)


class RedactionTests(TestCase):
    def test_purge_visitor_redacts_name_in_transcripts(self):
        admin = make_admin()
        visitor = make_visitor("Ana Maria Sousa")
        services.record_exchange(
            admin,
            None,
            question="Did Ana Maria Sousa arrive?",
            locale="en",
            result=reply("Yes, ANA MARIA SOUSA arrived at 08:05."),
        )

        purge_visitor(visitor)

        for message in ChatMessage.objects.all():
            self.assertNotIn("ana maria sousa", message.content.lower())
            self.assertIn(services.REDACTED, message.content)

    def test_redact_ignores_names_under_3_chars(self):
        self.assertEqual(services.redact_visitor("Al"), 0)


class RedactionReviewFixTests(TestCase):
    """Review findings 1 and 2: titles, and whole words only."""

    def test_purge_redacts_name_in_conversation_title(self):
        admin = make_admin()
        visitor = make_visitor("Ana Maria Sousa")
        conv, _, _ = services.record_exchange(
            admin, None, question="Did Ana Maria Sousa arrive?", locale="en", result=reply()
        )

        purge_visitor(visitor)

        conv.refresh_from_db()
        self.assertEqual(conv.title, f"Did {services.REDACTED} arrive?")

    def test_redaction_replaces_whole_words_only(self):
        admin = make_admin()
        visitor = make_visitor("Test")
        services.record_exchange(
            admin, None, question="latest contest by Test, fastest test", locale="en",
            result=reply("Test arrived; the latest scan was valid."),
        )

        purge_visitor(visitor)

        question, answer = ChatMessage.objects.order_by("id")
        self.assertEqual(question.content, f"latest contest by {services.REDACTED}, fastest {services.REDACTED}")
        self.assertEqual(answer.content, f"{services.REDACTED} arrived; the latest scan was valid.")

    def test_redaction_counts_only_rows_it_changed(self):
        admin = make_admin()
        services.record_exchange(admin, None, question="the latest figures", locale="en", result=reply())

        self.assertEqual(services.redact_visitor("Test"), 0)


class IdempotencyTests(TestCase):
    """Review finding 4: the same request id saves once."""

    def test_find_exchange_returns_the_stored_pair_for_its_owner_only(self):
        admin = make_admin()
        rid = "7b0f3c1e-9a43-4a7e-8a52-2d3c7e1f0a11"
        conv, q, a = services.record_exchange(
            admin, None, question="q", locale="en", result=reply("a"), client_id=rid
        )

        self.assertEqual(services.find_exchange(admin, rid), (conv, q, a))
        self.assertIsNone(services.find_exchange(make_admin("other"), rid))
