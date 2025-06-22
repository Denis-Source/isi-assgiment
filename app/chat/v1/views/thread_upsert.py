from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.serializers import ChatV1ThreadUpsertResponseSerializer
from chat.v1.services import ChatV1ThreadService
from common.base.views.base import BaseView
from common.swagger import SwaggerService


class ChatV1ThreadUpsertView(BaseView):
    """
    Retrieve a thread by a participant ID

    Retrieve a thread by a participant ID
    Create a new thread if it does not exist

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-thread-upsert"
    tags = ["Chat"]

    response_body_serializer_class = ChatV1ThreadUpsertResponseSerializer

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
    def post(self, _, participant_id: int, *args, **kwargs) -> Response:
        thread = self._service.upsert(
            user=self.request.user, participant_id=participant_id
        )

        return self._get_response(thread)
