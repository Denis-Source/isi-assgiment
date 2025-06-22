from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from auth_.v1.views import (
    AuthV1LoginView,
    AuthV1RefreshView,
    AuthV1RegistrationView,
)
from common.base.tests import BaseAPITestCase


class AuthV1LoginTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = reverse(AuthV1LoginView.name)
        self.valid_data = {
            "username": self.username,
            "password": self.password,
        }

    def test_success(self):
        response = self.client.post(self.url, self.valid_data)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response_json)
        self.assertTrue(RefreshToken(response_json["refresh"]))

    def test_not_exist(self):
        self.user.delete()

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_password(self):
        data = self.valid_data.copy()
        data["password"] = "wrong!!1_password"

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_username(self):
        data = self.valid_data.copy()
        del data["username"]

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        data = self.valid_data.copy()
        del data["password"]

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthV1RefreshTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = reverse(AuthV1RefreshView.name)

        self.refresh = str(RefreshToken.for_user(self.user))
        self.valid_data = {"refresh": self.refresh}

    def test_success(self):
        response = self.client.post(self.url, self.valid_data)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(AccessToken(response_json["access"]))

    def test_no_refresh(self):
        data = self.valid_data.copy()
        del data["refresh"]

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_refresh(self):
        data = self.valid_data.copy()
        data["refresh"] = "invalid"

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthV1RegistrationTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = reverse(AuthV1RegistrationView.name)
        self.user.delete()

        self.valid_data = {
            "username": self.username,
            "password": self.password,
        }

    def test_success(self):
        response = self.client.post(self.url, self.valid_data)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(RefreshToken(response_json["refresh"]))

    def test_no_username(self):
        data = self.valid_data.copy()
        del data["username"]

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_too_long(self):
        data = self.valid_data.copy()
        data["username"] = "invalid" * 100

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        data = self.valid_data.copy()
        del data["password"]

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_invalid(self):
        data = self.valid_data.copy()
        data["password"] = "invalid"

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_taken(self):
        data = self.valid_data.copy()
        data["username"] = self.another_user.username

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
