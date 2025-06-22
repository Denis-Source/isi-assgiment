from rest_framework import status
from rest_framework.exceptions import APIException


class UsernameTakenException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Username already taken"
