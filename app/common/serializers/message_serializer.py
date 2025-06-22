from rest_framework.fields import (
    CharField,
    IntegerField,
    JSONField,
    BooleanField,
)
from rest_framework.serializers import Serializer


class MessageSerializer(Serializer):
    detail = CharField(required=True)
    additional_field1 = BooleanField(required=False)
    additional_field2 = IntegerField(required=False)
    additional_field3 = JSONField(required=False)
