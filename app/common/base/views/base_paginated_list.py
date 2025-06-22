from urllib.parse import urlencode

from django.db.models import Model
from rest_framework.response import Response

from common.base.views.base import BaseView


class BasePaginatedListView(BaseView):
    paginated_response_body_serializer_class = None

    def _build_page_url(
        self, page: int, page_size: int, count: int
    ) -> str | None:
        if page < 1:
            return None

        if count is not None and (page - 1) * page_size >= count:
            return None

        query_params = self.request.query_params.dict()
        query_params.update({"page": page, "page_size": page_size})
        request_url = self.request.build_absolute_uri("?")
        return f"{request_url}?{urlencode(query_params)}"

    def _get_response_body_paginated(
        self,
        results: list[dict | Model],
        count: int,
        page: int,
        page_size: int,
        **kwargs,
    ) -> dict:
        return {
            "count": count,
            "next": self._build_page_url(page + 1, page_size, count),
            "previous": self._build_page_url(page - 1, page_size, count),
            "results": [self._get_response_body(data=d) for d in results],
            **kwargs,
        }

    def _get_response_paginated(
        self, results: list[dict | Model], count: int, **kwargs
    ) -> Response:
        request_data = self._get_request_query()

        page = request_data.get("page")
        page_size = request_data.get("page_size")

        response_data = self._get_response_body_paginated(
            results=results,
            count=count,
            page=page,
            page_size=page_size,
            **kwargs,
        )

        return Response(response_data, status=self.success_response_status)
