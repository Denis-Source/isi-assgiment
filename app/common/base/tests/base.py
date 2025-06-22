import logging

from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        logging.disable(logging.CRITICAL)
        self.maxDiff = None
        self.override = self.settings(
            DEBUG=True, PASSWORD_HASHING_ITERATIONS=10, SECRET_KEY="secret"
        )
        self.override.enable()
