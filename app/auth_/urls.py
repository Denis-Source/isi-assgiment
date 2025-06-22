from django.urls import path, include

urlpatterns = [
    path("v1/", include("auth_.v1.urls")),
]
