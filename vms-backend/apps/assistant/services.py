"""Saving conversations, and reading them back as the model's memory.

The model remembers a conversation because the server hands it the stored
history every turn -- the dashboard sends only the new message. A question and
its answer are written together, after the model has answered: a failed call
saves nothing, so retrying the same text never leaves a duplicate question.
"""

from __future__ import annotations

import re

from django.db import transaction
from django.utils import timezone

from .models import ChatMessage, ChatRole, Conversation

# Messages, not exchanges: ten questions and their answers. Enough for "and
# what about the 3rd?" to resolve; bounded so a long conversation does not
# grow the cost of every later question without limit.
HISTORY_LIMIT = 20
TITLE_CHARS = 80
REDACTED = "[deleted visitor]"


def get_owned(owner, conversation_id) -> Conversation:
    """The conversation, if this admin owns it. Anyone else's is DoesNotExist,
    exactly like a missing one -- an id must not confirm it exists."""
    return Conversation.objects.get(pk=conversation_id, owner=owner)


def history(conversation: Conversation | None) -> list[dict]:
    if conversation is None:
        return []
    latest = conversation.messages.order_by("-id")[:HISTORY_LIMIT]
    return [{"role": m.role, "content": m.content} for m in reversed(latest)]


def _title(question: str) -> str:
    first_line = question.strip().splitlines()[0].strip() if question.strip() else ""
    if len(first_line) <= TITLE_CHARS:
        return first_line
    return first_line[: TITLE_CHARS - 1].rstrip() + "…"


@transaction.atomic
def record_exchange(
    owner,
    conversation: Conversation | None,
    *,
    question: str,
    locale: str,
    result: dict,
    client_id=None,
) -> tuple[Conversation, ChatMessage, ChatMessage]:
    """Save a question and its answer together.

    `client_id` is the dashboard's id for this send. It is unique, so a retry
    of a request that already landed raises IntegrityError here instead of
    saving a second copy -- the caller answers with `find_exchange`.
    """
    if conversation is None:
        conversation = Conversation.objects.create(
            owner=owner, locale=locale, title=_title(question)
        )

    asked = ChatMessage.objects.create(
        conversation=conversation,
        role=ChatRole.USER,
        content=question,
        client_id=client_id,
    )
    answered = ChatMessage.objects.create(
        conversation=conversation,
        role=ChatRole.ASSISTANT,
        content=result["answer"],
        downloads=result.get("downloads", []),
        tools_used=result.get("tools_used", []),
    )

    # `auto_now` fires on save(), so this is what moves the conversation to the
    # top of the admin's history.
    conversation.updated_at = timezone.now()
    conversation.save(update_fields=["updated_at"])
    return conversation, asked, answered


def find_exchange(owner, client_id) -> tuple[Conversation, ChatMessage, ChatMessage] | None:
    """The question saved under `client_id` and the answer saved with it --
    only if this admin owns them. A request id must not reveal anyone else's."""
    question = (
        ChatMessage.objects.select_related("conversation")
        .filter(client_id=client_id, role=ChatRole.USER, conversation__owner=owner)
        .first()
    )
    if question is None:
        return None
    answer = (
        question.conversation.messages.filter(id__gt=question.id, role=ChatRole.ASSISTANT)
        .order_by("id")
        .first()
    )
    if answer is None:
        return None
    return question.conversation, question, answer


def redact_visitor(full_name: str) -> int:
    """Replace a purged visitor's full name in every saved message and title.

    Case-insensitive and WHOLE WORDS ONLY. A purge exists for test entries, so
    the obvious name is "Test": matched as a substring it turned every
    "latest" and "contest" in every admin's chats into "la[deleted visitor]",
    permanently. The lookarounds use `\\w`, which is Unicode-aware, so an
    accented letter counts as part of a word. Names under three characters
    are skipped as well -- even whole-word, "Al" is too ordinary to erase.

    Titles too: a conversation's title is its first question, which is where
    "Did Ana Maria Sousa arrive?" most often lives.

    Returns the number of rows actually changed.
    """
    name = full_name.strip()
    if len(name) < 3:
        return 0

    pattern = re.compile(rf"(?<!\w){re.escape(name)}(?!\w)", re.IGNORECASE)
    changed = 0

    for message in ChatMessage.objects.filter(content__icontains=name):
        redacted = pattern.sub(REDACTED, message.content)
        if redacted != message.content:
            message.content = redacted
            message.save(update_fields=["content"])
            changed += 1

    for conversation in Conversation.objects.filter(title__icontains=name):
        redacted = pattern.sub(REDACTED, conversation.title)
        if redacted != conversation.title:
            # Truncation keeps the column's limit if the marker is longer
            # than the name it replaced.
            conversation.title = redacted[:120]
            conversation.save(update_fields=["title"])
            changed += 1

    return changed
