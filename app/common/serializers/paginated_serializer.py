from rest_framework.fields import IntegerField, URLField
from rest_framework.serializers import Serializer


class BasePaginatedResponseSerializer(Serializer):
    count = IntegerField(required=True, min_value=0)
    next = URLField(allow_null=True, required=True)
    previous = URLField(allow_null=True, required=True)


class BasePaginatedRequestSerializer(Serializer):
    page = IntegerField(default=1, min_value=1, required=False)
    page_size = IntegerField(
        default=10, min_value=1, max_value=100, required=False
    )
