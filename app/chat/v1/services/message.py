from django.db.transaction import atomic
from django.utils.timezone import now
from rest_framework.exceptions import NotFound

from chat.models import Message, Thread
from common.base.services import BaseService


class ChatV1MessageService(BaseService):
    def _get_name(self):
        return "chat-v1-message-service"

    @atomic
    def create(self, user, thread_id: int, text: str) -> Message:
        thread = Thread.objects.filter(id=thread_id, participants=user).first()
        if not thread:
            self._logger.warn(
                f"Failed to created a message for {user}: thread not exist"
            )
            raise NotFound()

        message = Message.objects.create(thread=thread, sender=user, text=text)
        thread.updated_at = now()

        self._logger.info(f"Created message {message} for {user}")
        return message

    def read(self, user, message_id: int) -> Message:
        message = (
            Message.objects.filter(
                id=message_id,
                thread__participants=user,
                is_read=False,
            )
            .exclude(sender=user)
            .first()
        )
        if not message:
            self._logger.warn(
                f"Failed to read a message {message} for {user}: not found"
            )
            raise NotFound()

        message.is_read = True
        message.save()

        return message
