from django.db.models import TextChoices, QuerySet

from chat.models import Message
from common.base.services import BaseService
from common.pagination.offset_pagination import OffsetPaginationService


class ChatV1MessageListService(BaseService):
    def __init__(self):
        super().__init__()

        self._offset_pagination_service = OffsetPaginationService()

    class Orderings(TextChoices):
        CREATED_AT_ASC = "created_at"
        CREATED_AT_DESC = "-created_at"

    def _get_name(self):
        return "chat-v1-message-list-service"

    def _get_prefetch_qs(self, qs: QuerySet[Message]) -> QuerySet[Message]:
        return qs.prefetch_related("sender")

    def _get_filtered_qs(
        self, qs: QuerySet[Message], text: str = None, sender_id: int = None
    ) -> QuerySet[Message]:
        if text is not None:
            qs = qs.filter(text__icontains=text)

        if sender_id is not None:
            qs = qs.filter(sender_id=sender_id)

        return qs

    def _get_ordered_qs(
        self,
        qs: QuerySet[Message],
        ordering: Orderings = Orderings.CREATED_AT_DESC,
    ) -> QuerySet[Message]:
        return qs.order_by(ordering)

    def list(
        self,
        user,
        thread_id: int,
        text: str = None,
        sender_id: int = None,
        page: int = 1,
        page_size: int = 10,
        ordering: Orderings = Orderings.CREATED_AT_DESC,
    ) -> dict:
        qs = Message.objects.filter(thread_id=thread_id)
        prefetched_qs = self._get_prefetch_qs(qs)
        filtered_qs = self._get_filtered_qs(
            prefetched_qs,
            text=text,
            sender_id=sender_id,
        )
        ordered_qs = self._get_ordered_qs(filtered_qs, ordering=ordering)

        results = list(
            self._offset_pagination_service.paginate(
                iterable=ordered_qs, page=page, page_size=page_size
            )
        )
        total = ordered_qs.count()

        result = {
            "results": results,
            "count": total,
        }

        self._logger.info(f"Retrieved list of messages for {user}")

        return result
