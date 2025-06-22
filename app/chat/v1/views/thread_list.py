from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.v1.serializers import ChatV1ThreadListRequestSerializer
from chat.v1.serializers import (
    ChatV1ThreadListResponseSerializer,
    ChatV1ThreadListPaginatedResponseSerializer,
)
from chat.v1.services import ChatV1ThreadListService
from common.base.views.base_paginated_list import BasePaginatedListView
from common.swagger import SwaggerService


class ChatV1ThreadListView(BasePaginatedListView):
    """
    List threads

    Retrieve a paginated list of threads

    Authentication is required
    """

    permission_classes = [IsAuthenticated]

    name = "chat-v1-thread-list"
    tags = ["Chat"]

    request_query_serializer_class = ChatV1ThreadListRequestSerializer
    response_body_serializer_class = ChatV1ThreadListResponseSerializer
    paginated_response_body_serializer_class = (
        ChatV1ThreadListPaginatedResponseSerializer
    )

    success_response_status = status.HTTP_200_OK
    responses = {
        success_response_status: paginated_response_body_serializer_class(),
        **SwaggerService.generate_error_responses(
            ValidationError(),
            AuthenticationFailed(),
        ),
    }
    service_class = ChatV1ThreadListService

    @swagger_auto_schema(
        operation_id=name,
        tags=tags,
        query_serializer=request_query_serializer_class(),
        responses=responses,
    )
    def get(self, *args, **kwargs) -> Response:
        request_data = self._get_request_query()

        result = self._service.list(user=self.request.user, **request_data)

        return self._get_response_paginated(**result)
