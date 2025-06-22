from django.conf import settings
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from common.services import BaseService


class SwaggerService(BaseService):
    def _get_name(self):
        return "swagger-service"

    def get_schema(self):
        schema =  get_schema_view(
            Info(
                title=settings.APP_TITLE,
                default_version="v1",
            ),
            public=True,
            permission_classes=[AllowAny],
            url=settings.HOST,
        )

        self._logger.info("Generated swagger schema")
        return schema
