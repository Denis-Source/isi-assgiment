from django.contrib.auth import get_user_model
from django.db.models import TextChoices, QuerySet, Prefetch, Max

from chat.models import Thread, Message
from common.base.services import BaseService
from common.pagination.offset_pagination import OffsetPaginationService


class ChatV1ThreadListService(BaseService):
    def __init__(self):
        super().__init__()

        self._offset_pagination_service = OffsetPaginationService()

    class Orderings(TextChoices):
        CREATED_AT_ASC = "created_at"
        CREATED_AT_DESC = "-created_at"

        UPDATED_AT_ASC = "updated_at"
        UPDATED_AT_DESC = "-updated_at"

        LAST_MESSAGE_SENT_AT_ASC = "last_message_sent_at"
        LAST_MESSAGE_SENT_AT_DESC = "-last_message_sent_at"

    def _get_name(self):
        return "chat-v1-thread-list-service"

    def _get_prefetch_qs(self, qs: QuerySet[Thread]) -> QuerySet[Thread]:
        return qs.prefetch_related(
            Prefetch(
                "participants",
                queryset=get_user_model().objects.order_by("username"),
            )
        ).annotate(last_message_sent_at=Max("message__created_at"))

    def _get_filtered_qs(
        self, qs: QuerySet[Thread], participant_ids: list[int] = None
    ) -> QuerySet[Thread]:
        if participant_ids is not None:
            qs = qs.filter(participants__id__in=participant_ids)

        return qs

    def _get_ordered_qs(
        self,
        qs: QuerySet[Thread],
        ordering: Orderings = Orderings.CREATED_AT_DESC,
    ) -> QuerySet[Thread]:
        return qs.order_by(ordering)

    def _get_total_unread_messages(self, user) -> int:
        return (
            Message.objects.filter(thread__participants=user, is_read=False)
            .exclude(sender=user)
            .distinct()
            .count()
        )

    def list(
        self,
        user,
        participant_ids: list[int] = None,
        page: int = 1,
        page_size: int = 10,
        ordering: Orderings = Orderings.CREATED_AT_DESC,
    ) -> dict:
        qs = Thread.objects.all()
        prefetched_qs = self._get_prefetch_qs(qs)
        filtered_qs = self._get_filtered_qs(
            prefetched_qs, participant_ids=participant_ids
        )
        ordered_qs = self._get_ordered_qs(filtered_qs, ordering=ordering)

        results = list(
            self._offset_pagination_service.paginate(
                iterable=ordered_qs, page=page, page_size=page_size
            )
        )
        total = ordered_qs.count()
        total_unread = self._get_total_unread_messages(user=user)

        result = {
            "results": results,
            "count": total,
            "count_unread": total_unread,
        }

        self._logger.info(f"Retrieved list of threads for {user}")

        return result
