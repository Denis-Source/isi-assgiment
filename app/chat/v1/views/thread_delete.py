from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.services import ChatV1ThreadService
from common.base.serializers import MessageSerializer
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class ChatV1ThreadDeleteView(BaseView):
    """
    Delete a thread

    Delete a thread
    Can only be applied to threads in which the user is a participant

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-thread-delete"
    tags = ["Chat"]

    response_body_serializer_class = MessageSerializer

    success_response_status = status.HTTP_200_OK
    responses = {
        success_response_status: response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            AuthenticationFailed(), NotFound()
        ),
    }
    service_class = ChatV1ThreadService

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        responses=responses,
    )
    def delete(self, _, pk: int, *args, **kwargs) -> Response:
        self._service.delete(user=self.request.user, thread_id=pk)

        return self._get_response({"detail": "Thread has been deleted"})
