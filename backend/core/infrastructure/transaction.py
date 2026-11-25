from contextlib import AbstractContextManager
from django.db import transaction
from core.application.ports.transaction import TransactionManagerPort

class DjangoTransactionManager(TransactionManagerPort):
    def atomic(self) -> AbstractContextManager[None]:
        return transaction.atomic()