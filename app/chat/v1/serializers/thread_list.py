from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ChoiceField,
    IntegerField,
    ModelSerializer,
)

from chat.models import Thread
from chat.v1.services import ChatV1ThreadListService
from common.base.serializers import (
    BasePaginatedRequestSerializer,
    BasePaginatedResponseSerializer,
    CommaSeparatedListField,
)


class ChatV1ThreadListRequestSerializer(BasePaginatedRequestSerializer):
    participant_ids = CommaSeparatedListField(
        child=IntegerField(min_value=1), max_length=100, required=False
    )

    ordering = ChoiceField(
        choices=ChatV1ThreadListService.Orderings, required=False
    )


class ChatV1ThreadListParticipantResponseSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ChatV1ThreadListResponseSerializer(ModelSerializer):
    participants = ChatV1ThreadListParticipantResponseSerializer(many=True)

    class Meta:
        model = Thread
        fields = ["id", "participants"]


class ChatV1ThreadListPaginatedResponseSerializer(
    BasePaginatedResponseSerializer
):
    results = ChatV1ThreadListResponseSerializer(many=True)
    total_unread = IntegerField()
