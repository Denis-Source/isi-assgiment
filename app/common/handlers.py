from typing import Any

from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def json_handler404(request, exception):
    return JsonResponse(
        {"detail": "Requested resource does not exist"}, status=404
    )


def json_handler500(_):
    return JsonResponse({"detail": "Some error occurred"}, status=500)


def detail_exception_handler(exc: Exception, context: dict[str, Any]):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, ValidationError):
        response.data = {"detail": "Invalid data.", "fields": response.data}

    return response
