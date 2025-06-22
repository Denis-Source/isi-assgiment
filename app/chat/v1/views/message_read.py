from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.serializers import ChatV1MessageReadResponseSerializer
from chat.v1.services import ChatV1MessageService
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class ChatV1MessageReadView(BaseView):
    """
    Read a message in a thread

    Read a message in a thread

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-message-read"
    tags = ["Chat"]

    response_body_serializer_class = ChatV1MessageReadResponseSerializer

    success_response_status = status.HTTP_201_CREATED
    responses = {
        success_response_status: response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            AuthenticationFailed(), NotFound()
        ),
    }
    service_class = ChatV1MessageService

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        responses=responses,
    )
    def post(self, _, pk: int, *args, **kwargs) -> Response:
        message = self._service.read(user=self.request.user, message_id=pk)

        return self._get_response(message)
