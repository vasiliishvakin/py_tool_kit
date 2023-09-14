from datetime import datetime
from sortedcontainers import SortedSet


class TTLManager:
    def __init__(self):
        self._ttd: SortedSet = SortedSet()  # ttd = time to die
        self._ttd_keys: dict[int, set(str | int)] = {}
        self._keys_ttd: dict[str | int, int] = {}
        self._ttd_to_gc: set = set()

    def _set_ttd_key(self, ttd: int, key: str | int) -> None:
        if ttd not in self._ttd_keys:
            self._ttd_keys[ttd] = {key}
        else:
            self._ttd_keys[ttd].add(key)

    def _remove_ttd_key(self, ttd: int, key: str | int) -> None:
        if ttd in self._ttd_keys:
            if key in self._ttd_keys[ttd]:
                self._ttd_keys[ttd].remove(key)

    def get_ttd_keys(self, ttd: int) -> set[str]:
        return self._ttd_keys.get(ttd, set())

    def _set_key_ttd(self, key: str | int, ttd: int) -> None:
        self._keys_ttd[key] = ttd

    def _remove_key_ttd(self, key: str | int) -> None:
        if key in self._keys_ttd:
            del self._keys_ttd[key]

    def get_key_ttd(self, key: str | int) -> int | None:
        return self._keys_ttd.get(key)

    def _to_gc(self, ttd: int) -> None:
        self._ttd_to_gc.add(ttd)

    def _from_gc(self, ttd: int) -> None:
        if self._in_gc(ttd):
            self._ttd_to_gc.remove(ttd)

    def _in_gc(self, ttd: int) -> bool:
        return ttd in self._ttd_to_gc

    def gc_run(self) -> None:
        for ttd in self._ttd_to_gc:
            if ttd in self._ttd:
                self._ttd.remove(ttd)
        self._ttd_to_gc.clear()

    def set_ttd(self, key: str | int, ttl: int) -> int:
        current_time = int(datetime.now().timestamp())
        expiration_time = current_time + ttl
        self._ttd.add(expiration_time)
        self._set_ttd_key(expiration_time, key)
        self._set_key_ttd(key, expiration_time)
        self._from_gc(expiration_time)
        return expiration_time

    def remove_ttd(self, key: str | int) -> None:
        ttd = self.get_key_ttd(key)
        if ttd is not None:
            self._remove_ttd_key(ttd, key)
            self._remove_key_ttd(key)
            if len(self.get_ttd_keys(ttd)) == 0:
                self._to_gc(ttd)

    def get_expired_keys(self) -> list[str]:
        current_time = int(datetime.now().timestamp())
        expired_keys = []
        for ttd in self._ttd:
            if ttd > current_time:
                break
            expired_keys.extend(self.get_ttd_keys(ttd))
        return expired_keys

    def is_expired(self, key: str | int) -> bool:
        ttd = self.get_key_ttd(key)
        if ttd is None:
            return False  # Not expired, since there is no TTL set.
        current_time = int(datetime.now().timestamp())
        return current_time >= ttd

    def get_all_ttd(self) -> list[int]:
        return list(self._ttd)

    def get_all_keys(self) -> list[str]:
        return list(self._keys_ttd.keys())

    def clear(self) -> None:
        self._ttd.clear()
        self._ttd_keys.clear()
        self._keys_ttd.clear()
        self._ttd_to_gc.clear()
