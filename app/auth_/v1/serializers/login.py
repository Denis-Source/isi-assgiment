from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, ModelSerializer


class AuthV1LoginRequestSerializer(ModelSerializer):
    username = CharField(max_length=150)
    password = CharField(min_length=8, max_length=32, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class AuthV1LoginResponseSerializer(Serializer):
    refresh = CharField()
