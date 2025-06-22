from django.urls import path

from auth_.v1.views import (
    AuthV1LoginView,
    AuthV1RefreshView,
    AuthV1RegistrationView,
)

urlpatterns = [
    path("login/", AuthV1LoginView.as_view(), name=AuthV1LoginView.name),
    path("refresh/", AuthV1RefreshView.as_view(), name=AuthV1RefreshView.name),
    path(
        "registration/",
        AuthV1RegistrationView.as_view(),
        name=AuthV1RegistrationView.name,
    ),
]
