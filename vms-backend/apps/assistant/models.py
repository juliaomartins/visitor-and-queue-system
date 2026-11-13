"""What the assistant keeps: conversations, their messages, and memory notes.

PRIVATE PER ADMIN. Every row hangs off the admin who wrote it, and every query
in `services.py` and `memory.py` is scoped by owner. Nothing here is shared
between admins.

TRANSCRIPTS QUOTE VISITOR NAMES. An answer about who arrived names people, so
this is passport-adjacent data in the same sense as the visitor table, kept in
the same database under the same admin login. A permanent visitor delete
redacts their name from here (`services.redact_visitor`, called from
`purge_visitor`), or "erase for good" would leave them in chat history.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel, TimeStampedModel


class Locale(models.TextChoices):
    """The dashboard's three interface languages -- its `Locale` type exactly."""

    EN = "en", "English"
    PT = "pt", "Português"
    TET = "tet", "Tetun"


class Conversation(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assistant_conversations",
    )
    # The first question, cut short. Set once; later questions do not rename it.
    title = models.CharField(max_length=120, blank=True)
    # The interface language when the conversation began: the hint the model
    # falls back on for a message too short to tell its language.
    locale = models.CharField(max_length=8, choices=Locale.choices, default=Locale.EN)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [models.Index(fields=["owner", "-updated_at"])]

    def __str__(self) -> str:
        return self.title or str(self.pk)


class ChatRole(models.TextChoices):
    USER = "user", "User"
    ASSISTANT = "assistant", "Assistant"


class ChatMessage(TimeStampedModel):
    # Integer and monotonic: message order is insertion order, which a
    # timestamp cannot promise when two rows land in the same microsecond.
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=ChatRole.choices)
    content = models.TextField()
    # On an answer: the files it offered (the dashboard redraws the Download
    # buttons from these) and the tools that ran, for the record.
    downloads = models.JSONField(default=list, blank=True)
    tools_used = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:40]}"


class MemoryNote(BaseModel):
    """Something an admin asked the assistant to remember across conversations.

    Created only when the admin's own message asks for it, never containing a
    visitor's name -- see `memory.py` for both rules and why.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assistant_memories",
    )
    text = models.CharField(max_length=200)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.text
