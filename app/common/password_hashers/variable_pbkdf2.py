from django.conf import settings
from django.contrib.auth.hashers import PBKDF2PasswordHasher


class VariablePBKDF2PasswordHasher(PBKDF2PasswordHasher):
    def __init__(self, *args, **kwargs):
        self.iterations = settings.PASSWORD_HASHING_ITERATIONS
        super().__init__(*args, **kwargs)
