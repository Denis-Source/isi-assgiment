from django.urls import reverse
from rest_framework import status

from chat.models import Thread, Message
from chat.v1.services import ChatV1ThreadListService, ChatV1MessageListService
from chat.v1.views import (
    ChatV1ThreadUpsertView,
    ChatV1ThreadDeleteView,
    ChatV1ThreadListView,
)
from chat.v1.views.message_create import ChatV1MessageCreateView
from chat.v1.views.message_list import ChatV1MessageListView
from chat.v1.views.message_read import ChatV1MessageReadView
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


class ChatV1ThreadListTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = reverse(
            ChatV1ThreadListView.name,
        )
        self.params = {
            "page": 1,
            "page_size": 10,
            "participant_ids": [self.user.id, self.another_user.id],
            "ordering": ChatV1ThreadListService.Orderings.CREATED_AT_DESC,
        }
        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )
        self.message = Message.objects.create(
            sender=self.another_user, text="text", thread=self.thread
        )

    def test_success(self):
        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=self.params,
        )
        response_json = response.json()

        self.assertEqual(
            response_json,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "count_unread": 1,
                "results": [
                    {
                        "id": self.thread.id,
                        "participants": [
                            {
                                "id": self.another_user.id,
                                "username": self.another_user.username,
                            },
                            {
                                "id": self.user.id,
                                "username": self.user.username,
                            },
                        ],
                    }
                ],
            },
        )

    def test_invalid_participant_ids(self):
        params = self.params.copy()
        params["participant_ids"] = "invalid"

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_participant_ids_too_long(self):
        params = self.params.copy()
        params["participant_ids"] = [1, 2, 3] * 100

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_ordering(self):
        params = self.params.copy()
        params["ordering"] = "invalid"

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChatV1MessageCreateTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.text = "text"
        self.valid_data = {
            "text": self.text,
        }
        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )
        self.url = reverse(
            ChatV1MessageCreateView.name,
            kwargs={"pk": self.thread.id},
        )

    def test_success(self):
        response = self.client.post(
            self.url, data=self.valid_data, headers=self.get_auth_headers()
        )
        response_json = response.json()
        message_db = Message.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_json,
            {
                "id": message_db.id,
                "text": self.text,
                "is_read": message_db.is_read,
                "sender": {
                    "id": self.user.id,
                    "username": self.username,
                },
                "created_at": message_db.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            },
        )

    def test_text_too_long(self):
        data = self.valid_data
        data["text"] = "invalid" * 1000

        response = self.client.post(
            self.url, data=data, headers=self.get_auth_headers()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_text(self):
        data = self.valid_data
        del data["text"]

        response = self.client.post(
            self.url, data=data, headers=self.get_auth_headers()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_thread_not_exist(self):
        self.thread.delete()

        response = self.client.post(
            self.url, data=self.valid_data, headers=self.get_auth_headers()
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_authenticated(self):
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChatV1MessageReadTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )
        self.message = Message.objects.create(
            sender=self.another_user, text="text", thread=self.thread
        )
        self.url = reverse(
            ChatV1MessageReadView.name, kwargs={"pk": self.message.id}
        )

    def test_success(self):
        response = self.client.post(self.url, headers=self.get_auth_headers())
        response_json = response.json()
        self.message.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_json,
            {
                "id": self.message.id,
                "text": self.message.text,
                "is_read": True,
                "sender": {
                    "id": self.another_user.id,
                    "username": self.another_user.username,
                },
                "created_at": self.message.created_at.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            },
        )

    def test_message_not_exist(self):
        self.thread.delete()

        response = self.client.post(self.url, headers=self.get_auth_headers())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_authenticated(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChatV1MessageListTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )
        self.text = "text"
        self.message = Message.objects.create(
            sender=self.user, text=self.text, thread=self.thread
        )

        self.params = {
            "page": 1,
            "page_size": 10,
            "text": self.text,
            "sender_id": self.user.id,
            "ordering": ChatV1MessageListService.Orderings.CREATED_AT_DESC,
        }
        self.url = reverse(
            ChatV1MessageListView.name, kwargs={"pk": self.thread.id}
        )

    def test_success(self):
        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=self.params,
        )
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.message.id,
                        "text": self.text,
                        "sender": {
                            "id": self.user.id,
                            "username": self.username,
                        },
                        "is_read": self.message.is_read,
                        "created_at": self.message.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    }
                ],
            },
        )

    def test_sender_id_invalid(self):
        params = self.params.copy()
        params["sender_id"] = "invalid"

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_text_too_long(self):
        params = self.params.copy()
        params["text"] = "invalid" * 100

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_ordering(self):
        params = self.params.copy()
        params["ordering"] = "invalid"

        response = self.client.get(
            self.url,
            headers=self.get_auth_headers(),
            query_params=params,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
