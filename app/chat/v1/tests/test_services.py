from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from chat.models import Thread
from chat.v1.services import ChatV1ThreadService
from common.base.tests import BaseTestCase


class ChatV1ThreadServiceUpsertTestCase(BaseTestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="john_doe",
        )
        self.another_user = user_model.objects.create(
            username="another_john_doe",
        )
        self.service = ChatV1ThreadService()

    def test_success_retrieved(self):
        thread = Thread.objects.create()
        thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )

        result = self.service.upsert(
            user=self.user, participant_id=self.another_user.id
        )

        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(result, thread)

    def test_success_created(self):
        result = self.service.upsert(
            user=self.user, participant_id=self.another_user.id
        )
        result_db = Thread.objects.first()

        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(result_db, result)
        self.assertIn(self.user, result_db.participants.all())
        self.assertIn(self.another_user, result_db.participants.all())

    def test_no_another_user(self):
        self.another_user.delete()

        with self.assertRaises(NotFound):
            self.service.upsert(
                user=self.user, participant_id=self.another_user.id
            )

    def test_thread_with_self(self):
        with self.assertRaises(NotFound):
            self.service.upsert(user=self.user, participant_id=self.user.id)


class ChatV1ThreadServiceRemoveTestCase(BaseTestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="john_doe",
        )
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user, through_defaults={})
        self.service = ChatV1ThreadService()

    def test_success(self):
        self.service.delete(user=self.user, thread_id=self.thread.id)

        self.assertFalse(Thread.objects.filter(id=self.thread.id).exists())

    def test_not_exist(self):
        thread_id = self.thread.id
        self.thread.delete()

        with self.assertRaises(NotFound):
            self.service.delete(user=self.user, thread_id=thread_id)

    def test_not_participant(self):
        self.thread.participants.remove(self.user)

        with self.assertRaises(NotFound):
            self.service.delete(user=self.user, thread_id=self.thread.id)
