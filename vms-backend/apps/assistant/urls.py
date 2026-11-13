"""Assistant routes, mounted at /api/v1/ by config/urls.py."""

from django.urls import path

from .views import AssistantChatView, AssistantStatusView

urlpatterns = [
    path("assistant/chat", AssistantChatView.as_view(), name="assistant-chat"),
    path("assistant/status", AssistantStatusView.as_view(), name="assistant-status"),
]
