from django.urls import reverse
from rest_framework import status

from chat.models import Thread
from chat.v1.views import ChatV1ThreadUpsertView, ChatV1ThreadDeleteView
from common.base.tests import BaseAPITestCase


class ChatV1ThreadUpsertTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse(
            ChatV1ThreadUpsertView.name,
            kwargs={"participant_id": self.another_user.id},
        )
        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )

    def test_success(self):
        response = self.client.post(self.url, headers=self.get_auth_headers())
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            {
                "id": self.thread.id,
                "participants": [
                    {
                        "id": self.another_user.id,
                        "username": self.another_user.username,
                    },
                    {
                        "id": self.user.id,
                        "username": self.username,
                    },
                ],
            },
        )

    def test_not_exist(self):
        self.another_user.delete()

        response = self.client.post(self.url, headers=self.get_auth_headers())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_authenticated(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChatV1ThreadDeleteTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user, through_defaults={})

        self.url = reverse(
            ChatV1ThreadDeleteView.name, kwargs={"pk": self.thread.id}
        )

    def test_success(self):
        response = self.client.delete(
            self.url, headers=self.get_auth_headers()
        )
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            {
                "detail": "Thread has been deleted",
            },
        )

    def test_not_exist(self):
        self.thread.delete()

        response = self.client.delete(
            self.url, headers=self.get_auth_headers()
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_authenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
