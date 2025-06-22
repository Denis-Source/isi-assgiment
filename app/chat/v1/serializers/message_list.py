from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ChoiceField,
    IntegerField,
    ModelSerializer,
    CharField,
)

from chat.models import Message
from chat.v1.services import ChatV1MessageListService
from common.base.serializers import (
    BasePaginatedRequestSerializer,
    BasePaginatedResponseSerializer,
)


class ChatV1MessageListRequestSerializer(BasePaginatedRequestSerializer):
    text = CharField(max_length=512, required=False)
    sender_id = IntegerField(min_value=1, required=False)

    ordering = ChoiceField(
        choices=ChatV1MessageListService.Orderings, required=False
    )


class ChatV1MessageListSenderResponseSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ChatV1MessageListResponseSerializer(ModelSerializer):
    sender = ChatV1MessageListSenderResponseSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "is_read", "created_at"]


class ChatV1MessageListPaginatedResponseSerializer(
    BasePaginatedResponseSerializer
):
    results = ChatV1MessageListResponseSerializer(many=True)
