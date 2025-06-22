from django.urls import path

from chat.v1.views import (
    ChatV1ThreadUpsertView,
    ChatV1ThreadDeleteView,
    ChatV1ThreadListView,
)
from chat.v1.views.message_create import ChatV1MessageCreateView
from chat.v1.views.message_read import ChatV1MessageReadView

urlpatterns = [
    path(
        "threads/",
        ChatV1ThreadListView.as_view(),
        name=ChatV1ThreadListView.name,
    ),
    path(
        "threads/<int:participant_id>/",
        ChatV1ThreadUpsertView.as_view(),
        name=ChatV1ThreadUpsertView.name,
    ),
    path(
        "threads/<int:pk>/upsert/",
        ChatV1ThreadDeleteView.as_view(),
        name=ChatV1ThreadDeleteView.name,
    ),
    path(
        "threads/<int:pk>/messages/",
        ChatV1MessageCreateView.as_view(),
        name=ChatV1MessageCreateView.name,
    ),
    path(
        "messages/<int:pk>/read/",
        ChatV1MessageReadView.as_view(),
        name=ChatV1MessageReadView.name,
    ),
]
