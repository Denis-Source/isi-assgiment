from rest_framework.serializers import Serializer, CharField


class AuthV1LoginRequestSerializer(Serializer):
    username = CharField(max_length=150)
    password = CharField(min_length=8, max_length=32)


class AuthV1LoginResponseSerializer(Serializer):
    refresh = CharField()
