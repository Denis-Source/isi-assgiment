from django.urls import path, include

urlpatterns = [
    path("v1/", include("chat.v1.urls")),
]
