from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from auth_.exceptions import UsernameTakenException
from auth_.v1.services import AuthV1Service
from common.base.tests import BaseTestCase


class AuthV1ServiceLoginTestCase(BaseTestCase):
    def setUp(self):
        self.service = AuthV1Service()
        self.username = "johndoe"
        self.password = "SeccureP4assw0rd"
        usermodel = get_user_model()

        self.user = usermodel.objects.create(
            username=self.username,
        )
        self.user.set_password(self.password)
        self.user.save()

    def test_success(self):
        result = self.service.login(
            username=self.username, password=self.password
        )

        self.assertTrue(RefreshToken(result))

    def test_user_not_exist(self):
        self.user.delete()

        with self.assertRaises(AuthenticationFailed):
            self.service.login(username=self.username, password=self.password)

    def test_password_invalid(self):
        with self.assertRaises(AuthenticationFailed):
            self.service.login(username=self.username, password="invalid")


class AuthV1ServiceRefreshTestCase(BaseTestCase):
    def setUp(self):
        self.service = AuthV1Service()
        self.username = "johndoe"
        self.password = "SeccureP4assw0rd"
        usermodel = get_user_model()

        self.user = usermodel.objects.create(
            username=self.username,
        )
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_success(self):
        result = self.service.refresh(
            refresh=self.refresh_token,
        )

        self.assertTrue(AccessToken(result))

    def test_invalid_token(self):
        with self.assertRaises(AuthenticationFailed):
            self.service.refresh(
                refresh="invalid",
            )


class AuthV1ServiceRegisterTestCase(BaseTestCase):
    def setUp(self):
        self.service = AuthV1Service()
        self.username = "johndoe"
        self.password = "SeccureP4assw0rd"

    def test_success(self):
        result = self.service.register(
            username=self.username, password=self.password
        )

        self.assertTrue(RefreshToken(result))

    def test_username_taken(self):
        user_model = get_user_model()
        user_model.objects.create(
            username=self.username,
            password=self.password,
        )

        with self.assertRaises(UsernameTakenException):
            self.service.register(
                username=self.username, password=self.password
            )
