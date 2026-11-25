from contextlib import AbstractContextManager
from abc import ABC, abstractmethod

class TransactionManagerPort(ABC):
    @abstractmethod
    def atomic(self) -> AbstractContextManager[None]:
        pass