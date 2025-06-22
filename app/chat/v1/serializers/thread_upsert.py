from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from chat.models import Thread


class ChatV1ThreadUpsertParticipantResponseSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ChatV1ThreadUpsertResponseSerializer(ModelSerializer):
    participants = ChatV1ThreadUpsertParticipantResponseSerializer(many=True)

    class Meta:
        model = Thread
        fields = ["id", "participants"]
