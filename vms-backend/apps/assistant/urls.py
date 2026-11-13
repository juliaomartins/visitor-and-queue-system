"""Assistant routes, mounted at /api/v1/ by config/urls.py."""

from django.urls import path

from .views import (
    AssistantChatView,
    AssistantStatusView,
    ConversationDetailView,
    ConversationListView,
    MemoryDetailView,
    MemoryListView,
)

urlpatterns = [
    path("assistant/chat", AssistantChatView.as_view(), name="assistant-chat"),
    path("assistant/status", AssistantStatusView.as_view(), name="assistant-status"),
    path(
        "assistant/conversations",
        ConversationListView.as_view(),
        name="assistant-conversations",
    ),
    path(
        "assistant/conversations/<uuid:pk>",
        ConversationDetailView.as_view(),
        name="assistant-conversation",
    ),
    path("assistant/memories", MemoryListView.as_view(), name="assistant-memories"),
    path(
        "assistant/memories/<uuid:pk>",
        MemoryDetailView.as_view(),
        name="assistant-memory",
    ),
]
