from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_.v1.serializers import (
    AuthV1LoginRequestSerializer,
    AuthV1LoginResponseSerializer,
)
from auth_.v1.services import AuthV1Service
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class AuthV1LoginView(BaseView):
    """
    Return access and refresh tokens

    Return access and refresh tokens if provided credentials are correct

    Authentication is not required
    """

    permission_classes = [AllowAny]

    name = "auth-v1-login"
    tags = ["Auth"]

    request_body_serializer_class = AuthV1LoginRequestSerializer
    response_body_serializer_class = AuthV1LoginResponseSerializer

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

        refresh = self._service.login(**data)

        return self._get_response({"refresh": refresh})
