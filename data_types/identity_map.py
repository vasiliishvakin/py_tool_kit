from typing import Iterator, Any, Callable


class IdentityMap:
    def __init__(self):
        self._items = {}

    def has(self, key: str | int) -> bool:
        return key in self._items

    def get(self, key: str | int) -> Any | None:
        return self._items.get(key)

    def get_or_fetch(self, key: str | int, loader: Callable[[], Any]) -> Any:
        data = self.get(key)
        if data is not None:
            return data

        data = loader()
        self.add(key, data)
        return data

    def add(self, key: str | int, data: Any) -> None:
        self._items[key] = data

    def update(self, key: str | int, data: Any) -> None:
        if key in self._items:
            self._items[key] = data

    def remove(self, key: str | int) -> bool:
        if key in self._items:
            del self._items[key]
            return True
        return False

    def clear(self) -> None:
        self._items.clear()

    def keys(self):
        return self._items.keys()

    def __len__(self) -> int:
        """Return the count of objects in the IdentityMap."""
        return len(self._items)

    def __iter__(self) -> Iterator[str]:
        """Iterate over the keys (IDs) in the IdentityMap."""
        return iter(self._items)
