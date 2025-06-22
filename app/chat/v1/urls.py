from django.urls import path

from chat.v1.views import (
    ChatV1ThreadUpsertView,
    ChatV1ThreadDeleteView,
    ChatV1ThreadListView,
)

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
        "threads/<int:pk>/delete/",
        ChatV1ThreadDeleteView.as_view(),
        name=ChatV1ThreadDeleteView.name,
    ),
]
