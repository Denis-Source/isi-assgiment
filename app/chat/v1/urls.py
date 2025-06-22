from django.urls import path

from chat.v1.views import ChatV1ThreadUpsertView

urlpatterns = [
    path(
        "thread/upsert/<int:pk>/",
        ChatV1ThreadUpsertView.as_view(),
        name=ChatV1ThreadUpsertView.name,
    ),
]
