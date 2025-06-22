from common.base.services import BaseService


class OffsetPaginationService(BaseService):
    def _get_name(self):
        return "offset-pagination-service"

    def paginate(self, iterable: iter, page: int, page_size: int) -> list:
        offset = (page - 1) * page_size
        result = iterable[offset : offset + page_size]

        return result
