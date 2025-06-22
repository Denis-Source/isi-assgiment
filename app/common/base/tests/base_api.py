from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from common.base.tests import BaseTestCase


class BaseAPITestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.username = "johndoe"
        self.password = "SeccureP4assw0rd"

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=self.username,
        )
        self.user.set_password(self.password)
        self.user.save()

        self.another_user = user_model.objects.create(
            username="another_john_doe",
        )
        self.another_user.set_password("AnotheSeccureP4assw0rd")
        self.another_user.save()

    def get_auth_headers(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def get_access_token(self) -> str:
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)
