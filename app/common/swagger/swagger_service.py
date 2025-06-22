from django.conf import settings
from drf_yasg.openapi import Info
from drf_yasg.openapi import Response
from drf_yasg.views import get_schema_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from common.base.serializers import MessageSerializer
from common.base.services import BaseService


class ExceptionResponse(Response):
    def __init__(self, *exceptions: APIException):
        description = self._get_description(*exceptions)
        super().__init__(description=description, schema=MessageSerializer())

    def _get_description(self, *exceptions: APIException) -> str:
        return "\n".join(
            str(exception.default_detail) for exception in exceptions
        )


class SwaggerService(BaseService):
    def _get_name(self):
        return "swagger-service"

    @staticmethod
    def generate_error_responses(
        *exceptions: APIException,
    ) -> dict[int, Response]:
        exception_map = {}

        for exception in exceptions:
            if exception.status_code not in exception_map:
                exception_map[exception.status_code] = [exception]
            else:
                exception_map[exception.status_code].append(exception)

        return {
            status: ExceptionResponse(*exceptions)
            for status, exceptions in exception_map.items()
        }

    @staticmethod
    def get_schema():
        return get_schema_view(
            Info(
                title=settings.APP_TITLE,
                default_version="v1",
            ),
            public=True,
            permission_classes=[AllowAny],
            url=settings.HOST,
        )
