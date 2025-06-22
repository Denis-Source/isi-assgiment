from django.urls import path

from chat.v1.views import (
    ChatV1ThreadUpsertView,
    ChatV1ThreadDeleteView,
    ChatV1ThreadListView,
)

urlpatterns = [
    path(
        "thread/",
        ChatV1ThreadListView.as_view(),
        name=ChatV1ThreadListView.name,
    ),
    path(
        "thread/<int:participant_id>/",
        ChatV1ThreadUpsertView.as_view(),
        name=ChatV1ThreadUpsertView.name,
    ),
    path(
        "thread/<int:pk>/delete/",
        ChatV1ThreadDeleteView.as_view(),
        name=ChatV1ThreadDeleteView.name,
    ),
]
