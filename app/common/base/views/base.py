from django.db.models import Model
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class ResponseSerializationMismatch(Exception):
    pass


class BaseAPIView(APIView):
    name = None
    tags = None

    service_class = None

    request_body_serializer_class = None
    request_query_serializer_class = None
    response_body_serializer_class = None

    success_response_status = None
    responses = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.service_class is None:
            # DRF calls base class before a child one
            # (weird DRF behavior)
            return

        self._service = self.service_class()

    def _get_request_query(self) -> dict:
        if not self.request_query_serializer_class:
            raise NotImplementedError(
                "Request query serializer class is not set"
            )

        serializer = self.request_query_serializer_class(
            data=self.request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def _get_request_body(self) -> dict:
        if not self.request_body_serializer_class:
            raise NotImplementedError(
                "Request body serializer class is not set"
            )

        serializer = self.request_body_serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def _get_response_body(self, data: dict | Model) -> dict:
        if not self.response_body_serializer_class:
            raise NotImplementedError(
                "Response body serializer class is not set"
            )

        if isinstance(data, Model):
            serializer = self.response_body_serializer_class(instance=data)
            return serializer.data

        if isinstance(data, dict):
            serializer = self.response_body_serializer_class(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                return serializer.validated_data
            except ValidationError as e:
                raise ResponseSerializationMismatch from e

        raise NotImplementedError("Not supported data type")

    def _get_response(self, data: dict | Model) -> Response:
        response_data = self._get_response_body(data=data)

        return Response(response_data, status=self.success_response_status)
