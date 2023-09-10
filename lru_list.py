from collections import deque
from typing import Iterator, List, Any


class LRUList:
    def __init__(self):
        self._lru = deque()

    def has(self, key: str | int) -> bool:
        return key in self._lru

    def add(self, key: str | int) -> bool:
        if self.has(key):
            return False
        self._lru.append(key)
        return True

    def remove(self, key: str | int) -> bool:
        try:
            self._lru.remove(key)
            return True
        except ValueError:
            return False

    def update(self, key) -> bool:
        if not self.has(key):
            return False
        self.remove(key)
        return self.add(key)

    def upsert(self, key) -> bool:
        return self.update(key) or self.add(key)

    def get_last(self, count: int) -> List[Any]:
        """
        This method returns a list containing the count most recently used elements from the LRUList.
        In other words, it retrieves the count elements that were added or accessed most recently in the list.
        The elements are returned in the order in which they were added or accessed,
        with the most recent key at the end of the returned list.
        """
        return list(self._lru)[-count:]

    def get_first(self, count: int) -> List[Any]:
        """
        this method returns a list containing the count least recently used elements from the LRUList.
        It retrieves the count elements that were added or accessed least recently in the list.
        The elements are returned in the order in which they were added or accessed,
        with the least recent key at the beginning of the returned list.
        """
        return list(self._lru)[:count]

    def __len__(self) -> int:
        """Return the count of objects in the LRUList."""
        return len(self._lru)

    def data(self) -> List[str]:
        return list(self._lru)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the values in the LRUList."""
        return iter(self._lru)

    def clear(self) -> None:
        self._lru.clear()
