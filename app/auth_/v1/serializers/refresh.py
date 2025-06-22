from rest_framework.fields import CharField
from rest_framework.serializers import Serializer


class AuthV1RefreshRequestSerializer(Serializer):
    refresh = CharField()


class AuthV1RefreshResponseSerializer(Serializer):
    access = CharField()
