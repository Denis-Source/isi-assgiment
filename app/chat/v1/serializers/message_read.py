from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from chat.models import Message


class ChatV1MessageSenderReadResponseSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ChatV1MessageReadResponseSerializer(ModelSerializer):
    sender = ChatV1MessageSenderReadResponseSerializer()

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "is_read", "created_at"]
