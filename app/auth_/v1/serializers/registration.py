from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, Serializer, CharField


class AuthV1RegistrationRequestSerializer(ModelSerializer):
    username = CharField(max_length=150)
    password = CharField(min_length=8, max_length=32)

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

    def validate_password(self, value: str):
        validate_password(value)
        return value


class AuthV1RegistrationResponseSerializer(Serializer):
    refresh = CharField(required=True)
