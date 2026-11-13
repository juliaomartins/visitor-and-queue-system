from django.apps import AppConfig


class AssistantConfig(AppConfig):
    """The dashboard's chat assistant. NO MODELS — it reads visitors and scans."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.assistant"
    label = "assistant"
