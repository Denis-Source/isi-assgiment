from common.handlers import json_handler404, json_handler500
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from common.swagger import SwaggerService

swagger_service = SwaggerService()
swagger_schema = swagger_service.get_schema()

handler404 = json_handler404
if not settings.DEBUG:
    handler500 = json_handler500

urlpatterns = []

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += (
    path(
        "",
        swagger_schema.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
)
