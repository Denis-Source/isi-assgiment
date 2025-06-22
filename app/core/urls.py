from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from common.handlers import json_handler404, json_handler500
from common.swagger import SwaggerService

handler404 = json_handler404
if not settings.DEBUG:
    handler500 = json_handler500

urlpatterns = [
    path(
        "",
        SwaggerService.get_schema().with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("auth/", include("auth.v1.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
