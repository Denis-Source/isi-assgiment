from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.serializers import (
    ChatV1MessageListRequestSerializer,
    ChatV1MessageListResponseSerializer,
    ChatV1MessageListPaginatedResponseSerializer,
)
from chat.v1.services import ChatV1MessageListService
from common.base.views.base_paginated_list import BasePaginatedListView
from common.swagger import SwaggerService


class ChatV1MessageListView(BasePaginatedListView):
    """
    List messages for a thread

    Retrieve a paginated list of messages in a thread

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-message-list"
    tags = ["Chat"]

    request_query_serializer_class = ChatV1MessageListRequestSerializer
    response_body_serializer_class = ChatV1MessageListResponseSerializer
    paginated_response_body_serializer_class = (
        ChatV1MessageListPaginatedResponseSerializer
    )

    success_response_status = status.HTTP_200_OK
    responses = {
        success_response_status: paginated_response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            ValidationError(),
            AuthenticationFailed(),
        ),
    }
    service_class = ChatV1MessageListService

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        query_serializer=request_query_serializer_class(),
        responses=responses,
    )
    def get(self, _, pk: int, *args, **kwargs) -> Response:
        request_data = self._get_request_query()

        result = self._service.list(
            user=self.request.user, thread_id=pk, **request_data
        )

        return self._get_response_paginated(**result)
