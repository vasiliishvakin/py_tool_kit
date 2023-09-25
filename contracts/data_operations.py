from abc import ABC, abstractmethod
from typing import Any


class CRUD(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class CRUDL(CRUD):
    @abstractmethod
    def all(self):
        pass

    def filter(self, *criterion):
        pass

    def count(self):
        pass


class BulkOperations(ABC):
    @abstractmethod
    def bulk_update(self):
        pass

    @abstractmethod
    def bulk_delete(self):
        pass


class IDBasedOperations(ABC):
    @abstractmethod
    def delete_by_id(self):
        pass


class Transformable(ABC):
    @abstractmethod
    def create_from_dict(self, dict) -> Any:
        pass


class Transactional(ABC):
    @abstractmethod
    def begin_transaction(self):
        pass

    @abstractmethod
    def commit_transaction(self):
        pass

    @abstractmethod
    def rollback_transaction(self):
        pass
