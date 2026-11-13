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
) -> tuple[Conversation, ChatMessage, ChatMessage]:
    if conversation is None:
        conversation = Conversation.objects.create(
            owner=owner, locale=locale, title=_title(question)
        )

    asked = ChatMessage.objects.create(
        conversation=conversation, role=ChatRole.USER, content=question
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


def redact_visitor(full_name: str) -> int:
    """Replace a purged visitor's full name in every saved message.

    Case-insensitive, whole name only. Names under three characters are
    skipped: replacing "Al" everywhere would deface ordinary words in every
    transcript, which is worse than the trace it removes.
    """
    name = full_name.strip()
    if len(name) < 3:
        return 0

    pattern = re.compile(re.escape(name), re.IGNORECASE)
    changed = 0
    for message in ChatMessage.objects.filter(content__icontains=name):
        message.content = pattern.sub(REDACTED, message.content)
        message.save(update_fields=["content"])
        changed += 1
    return changed
