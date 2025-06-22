from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    ValidationError,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.serializers.message_create import (
    ChatV1MessageCreateRequestSerializer,
    ChatV1MessageCreateResponseSerializer,
)
from chat.v1.services import ChatV1MessageService
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class ChatV1MessageCreateView(BaseView):
    """
    Create a message in a thread

    Create a message in a thread

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-message-create"
    tags = ["Chat"]

    request_body_serializer_class = ChatV1MessageCreateRequestSerializer
    response_body_serializer_class = ChatV1MessageCreateResponseSerializer

    success_response_status = status.HTTP_201_CREATED
    responses = {
        success_response_status: response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            ValidationError(), AuthenticationFailed(), NotFound()
        ),
    }
    service_class = ChatV1MessageService

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        responses=responses,
    )
    def post(self, _, pk: int, *args, **kwargs) -> Response:
        data = self._get_request_body()
        message = self._service.create(
            user=self.request.user, thread_id=pk, **data
        )

        return self._get_response(message)
