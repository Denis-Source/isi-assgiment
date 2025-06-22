from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from auth_.exceptions import UsernameTakenException
from common.base.services import BaseService


class AuthV1Service(BaseService):
    def _get_name(self):
        return "auth-v1-service"

    def login(self, username: str, password: str) -> str:
        user_model = get_user_model()
        user = user_model.objects.filter(username=username).first()
        if not user:
            self._logger.warn(
                f"Failed to generate refresh token for {username}: not found"
            )
            raise AuthenticationFailed()

        if not user.check_password(password):
            self._logger.warn(
                f"Failed to generate refresh token for {user}: "
                f"invalid password"
            )
            raise AuthenticationFailed()

        refresh = RefreshToken.for_user(user)

        self._logger.warn(f"Generated refresh token for {user}")
        return str(refresh)

    def refresh(self, refresh: str) -> str:
        try:
            token = RefreshToken(refresh)
        except TokenError:
            self._logger.warn(
                "Failed to generate access token: invalid refresh token"
            )
            raise AuthenticationFailed("Invalid refresh token")

        self._logger.warn("Generated access token")
        return str(token.access_token)

    def register(self, username: str, password: str) -> str:
        user_model = get_user_model()

        try:
            user = user_model.objects.create(
                username=username,
                password=password,
            )
        except IntegrityError as e:
            self._logger.warn(f"Failed to register {username}: username taken")
            raise UsernameTakenException() from e

        refresh = RefreshToken.for_user(user)

        self._logger.warn(f"Registered user {user}")
        return str(refresh)
