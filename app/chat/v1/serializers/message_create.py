from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from chat.models import Message


class ChatV1MessageCreateRequestSerializer(Serializer):
    text = CharField(max_length=2048, required=True)


class ChatV1MessageSenderCreateResponseSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ChatV1MessageCreateResponseSerializer(ModelSerializer):
    sender = ChatV1MessageSenderCreateResponseSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "is_read", "created_at"]
