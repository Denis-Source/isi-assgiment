from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_.v1.serializers import (
    AuthV1RefreshResponseSerializer,
    AuthV1RefreshRequestSerializer,
)
from auth_.v1.services import AuthV1Service
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class AuthV1RefreshView(BaseView):
    """
    Return access token

    Return access token if refresh token is valid

    Authentication is not required
    """

    permission_classes = [AllowAny]

    name = "auth-v1-refresh"
    tags = ["Auth"]

    request_body_serializer_class = AuthV1RefreshRequestSerializer
    response_body_serializer_class = AuthV1RefreshResponseSerializer

    success_response_status = status.HTTP_200_OK
    responses = {
        success_response_status: response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            ValidationError(),
            AuthenticationFailed(),
        ),
    }
    service_class = AuthV1Service

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        request_body=request_body_serializer_class(),
        responses=responses,
    )
    def post(self, *args, **kwargs) -> Response:
        data = self._get_request_body()

        access = self._service.refresh(**data)

        return self._get_response({"access": access})
