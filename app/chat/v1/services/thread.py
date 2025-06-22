from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Prefetch
from django.db.transaction import atomic
from rest_framework.exceptions import NotFound

from chat.models import Thread
from common.base.services import BaseService


class ChatV1ThreadService(BaseService):
    PARTICIPANT_LIMIT = 2

    def _get_name(self):
        return "chat-v1-thread-service"

    def _get_thread_by_participant_ids(
        self, participant_ids: list[int]
    ) -> Thread | None:
        count = len(participant_ids)
        participant_count_qs = Count(
            "participants",
            filter=Q(participants__id__in=participant_ids),
            distinct=True,
        )
        return (
            Thread.objects.annotate(participant_count=participant_count_qs)
            .filter(participant_count=count)
            .prefetch_related(self._get_thread_prefetch())
            .first()
        )

    def _get_thread_prefetch(self) -> Prefetch:
        return Prefetch(
            "participants",
            queryset=get_user_model().objects.order_by("username"),
        )

    def _create_thread_by_participants(self, participants: list) -> Thread:
        thread = Thread.objects.create()
        thread.participants.add(*participants, through_defaults={})
        return Thread.objects.prefetch_related(
            self._get_thread_prefetch()
        ).get(id=thread.id)

    @atomic
    def upsert(self, user, participant_id: str) -> Thread:
        user_model = get_user_model()
        another_user = (
            user_model.objects.filter(id=participant_id)
            .exclude(id=user.id)
            .first()
        )
        if not another_user:
            self._logger.warn(
                f"Failed to upsert a thread for {user}:"
                f" another participant {participant_id} not exist"
            )
            raise NotFound("User does not exist")

        thread = self._get_thread_by_participant_ids(
            participant_ids=[user.id, participant_id]
        )
        if not thread:
            thread = self._create_thread_by_participants(
                participants=[user, another_user]
            )
            self._logger.info(
                f"Created a new thread between {user} and {another_user}"
                f" for {user}"
            )

        self._logger.info(
            f"Retrieved a thread between {user} and {another_user}"
            f" for {user}"
        )
        return thread

    def delete(self, user, thread_id: int) -> None:
        thread = Thread.objects.filter(
            id=thread_id, participants__in=[user.id]
        ).first()
        if not thread:
            self._logger.warn(f"Failed to delete thread for {user}: not found")
            raise NotFound()

        thread.delete()
        self._logger.info(f"Deleted thread {thread} for {user}")
