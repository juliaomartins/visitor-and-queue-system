"""Request and response shapes for the assistant. They become `@vms/contracts`."""

from rest_framework import serializers

from apps.scans.models import ScanResult
from apps.visitors.models import VisitorCategory

# The dashboard sends the visible transcript every turn. Bounded so one request
# cannot ship a novel to OpenAI on the admin's key.
MAX_MESSAGES = 20
MAX_MESSAGE_CHARS = 4000


class ChatMessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "assistant"])
    content = serializers.CharField(max_length=MAX_MESSAGE_CHARS, trim_whitespace=True)


class ChatRequestSerializer(serializers.Serializer):
    messages = ChatMessageSerializer(many=True, min_length=1, max_length=MAX_MESSAGES)

    def validate_messages(self, value):
        if value[-1]["role"] != "user":
            raise serializers.ValidationError("The last message must be the user's.")
        return value


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


class ChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    downloads = DownloadOfferSerializer(many=True)
    tools_used = serializers.ListField(child=serializers.CharField())


class AssistantStatusSerializer(serializers.Serializer):
    enabled = serializers.BooleanField()
    model = serializers.CharField()
