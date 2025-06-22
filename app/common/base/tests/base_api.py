from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from common.base.tests import BaseTestCase


class BaseAPITestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.password = "SeccureP4assw0rd"
        self.username = "johndoe"

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.another_user = user_model.objects.create(
            username="another_john_doe",
            password="PAsaossaoah!21",
        )

    def get_auth_headers(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def get_access_token(self) -> str:
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)
