from abc import ABC, abstractmethod

from logging import getLogger


class BaseService(ABC):
    def __init__(self):
        self._logger = getLogger(self._get_name())

    @abstractmethod
    def _get_name(self):
        pass
