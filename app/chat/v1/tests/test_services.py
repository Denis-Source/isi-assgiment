from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from chat.models import Thread, Message
from chat.v1.services import ChatV1ThreadService, ChatV1ThreadListService
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


class ChatV1ThreadListServiceTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user_model = get_user_model()

        self.service = ChatV1ThreadListService()
        self.user = user_model.objects.create(
            username="john_doe",
        )
        self.another_user = user_model.objects.create(
            username="another_john_doe",
        )
        self.different_user = user_model.objects.create(
            username="dave",
        )

        self.thread = Thread.objects.create()
        self.thread.participants.add(
            self.user, self.another_user, through_defaults={}
        )
        self.another_thread = Thread.objects.create()
        self.another_thread.participants.add(
            self.user, self.different_user, through_defaults={}
        )

        self.message = Message.objects.create(
            text="text", sender=self.another_user, thread=self.thread
        )

        self.another_message = Message.objects.create(
            is_read=True,
            text="text",
            sender=self.user,
            thread=self.another_thread,
        )

    def test_defaults(self):
        result = self.service.list(
            user=self.user,
        )

        self.assertEqual(
            result["results"],
            [
                self.another_thread,
                self.thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_filter_by_participant(self):
        result = self.service.list(
            user=self.user, participant_ids=[self.another_user.id]
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
            ],
        )
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_created_at_asc(self):
        result = self.service.list(
            user=self.user, ordering=self.service.Orderings.CREATED_AT_ASC
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_created_at_desc(self):
        self.thread.created_at = self.another_thread.created_at + timedelta(
            minutes=5
        )
        self.thread.save()

        result = self.service.list(
            user=self.user, ordering=self.service.Orderings.CREATED_AT_DESC
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_updated_at_asc(self):
        self.another_thread.created_at = self.thread.updated_at + timedelta(
            minutes=5
        )
        self.another_thread.save()

        result = self.service.list(
            user=self.user, ordering=self.service.Orderings.UPDATED_AT_ASC
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_updated_at_desc(self):
        self.thread.updated_at = self.another_thread.updated_at + timedelta(
            minutes=5
        )
        self.thread.save()

        result = self.service.list(
            user=self.user, ordering=self.service.Orderings.UPDATED_AT_DESC
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_last_message_sent_at_asc(self):
        result = self.service.list(
            user=self.user,
            ordering=self.service.Orderings.LAST_MESSAGE_SENT_AT_ASC,
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)

    def test_order_by_last_message_sent_at_desc(self):
        self.message.created_at = self.another_message.created_at + timedelta(
            minutes=5
        )
        self.message.save()

        result = self.service.list(
            user=self.user,
            ordering=self.service.Orderings.LAST_MESSAGE_SENT_AT_DESC,
        )

        self.assertEqual(
            result["results"],
            [
                self.thread,
                self.another_thread,
            ],
        )
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["total_unread"], 1)
