"""Request and response shapes for the assistant. They become `@vms/contracts`."""

from rest_framework import serializers

from apps.scans.models import ScanResult
from apps.visitors.models import VisitorCategory

from .models import ChatMessage, Conversation, Locale, MemoryNote

# One question per request. Bounded so a pasted document cannot be shipped to
# OpenAI on the admin's key; the history the model also sees is bounded by
# services.HISTORY_LIMIT.
MAX_MESSAGE_CHARS = 4000


class ChatRequestSerializer(serializers.Serializer):
    """Only the new message. The history comes from the database, not the
    browser -- so a reload loses nothing and a client cannot rewrite the past."""

    conversation = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(max_length=MAX_MESSAGE_CHARS, trim_whitespace=True)
    locale = serializers.ChoiceField(choices=Locale.choices, default=Locale.EN)
    # The dashboard's id for this send, reused by Retry. A send that already
    # landed is answered from the database instead of being asked again.
    request_id = serializers.UUIDField(required=False, allow_null=True)


class DownloadFiltersSerializer(serializers.Serializer):
    date_from = serializers.DateField(allow_null=True)
    date_to = serializers.DateField(allow_null=True)
    country = serializers.CharField(allow_null=True)
    # The models' own choices, so the schema reuses CategoryEnum / ResultEnum
    # rather than minting a colliding second enum of the same name.
    category = serializers.ChoiceField(choices=VisitorCategory.choices, allow_null=True)
    result = serializers.ChoiceField(choices=ScanResult.choices, allow_null=True)


class DownloadOfferSerializer(serializers.Serializer):
    """A file the answer offers. The dashboard fetches it from the export view."""

    report = serializers.ChoiceField(choices=["entrance_report", "visitor_list"])
    format = serializers.ChoiceField(choices=["pdf", "xlsx", "csv"])
    filters = DownloadFiltersSerializer()


class ChatMessageSerializer(serializers.ModelSerializer):
    downloads = DownloadOfferSerializer(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ("id", "role", "content", "downloads", "created_at")
        read_only_fields = fields


class ConversationSummarySerializer(serializers.ModelSerializer):
    # Annotated by the views (`Count("messages")`), never a query per row.
    message_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "title", "locale", "created_at", "updated_at", "message_count")
        read_only_fields = fields


class ConversationDetailSerializer(ConversationSummarySerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta(ConversationSummarySerializer.Meta):
        fields = (*ConversationSummarySerializer.Meta.fields, "messages")
        read_only_fields = fields


class ChatResponseSerializer(serializers.Serializer):
    conversation = ConversationSummarySerializer()
    question = ChatMessageSerializer()
    answer = ChatMessageSerializer()
    # Notes saved on this turn, so the dashboard can say "Remembered: …".
    remembered = serializers.ListField(child=serializers.CharField())


class ConversationRenameSerializer(serializers.Serializer):
    """`PATCH /assistant/conversations/{id}`: the title, and nothing else."""

    title = serializers.CharField(max_length=120, trim_whitespace=True)


class MemoryNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryNote
        fields = ("id", "text", "created_at")
        read_only_fields = fields


class AssistantStatusSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()
    model = serializers.CharField()
