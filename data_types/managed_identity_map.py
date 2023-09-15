from typing import Any, Callable, Iterator, List, TypedDict, Unpack

from .import HitsMisses, IdentityMap, LRUList, TagsManager, TTLManager, GCType, GCOperator


class IdentityMapAddParams(TypedDict):
    ttl: int | None
    tags: List[str] | tuple[str] | None


class IdentityMapInfo:
    def __init__(
        self,
        is_expired: Callable[[], bool] | None | bool = None,
        is_deleted: bool = False,
        stats: dict[str, Any] | None = None,
    ):
        self.id_deleted: bool = is_deleted
        self._is_expired: Callable[[], bool] | None | bool = is_expired
        self.stats: dict[str, Any] | None = stats

    @property
    def is_expired(self) -> bool:
        if self._is_expired is None:
            self._is_expired = False
        elif callable(self._is_expired):
            is_expired = self._is_expired()
            if is_expired:
                self._is_expired = True
            return is_expired

        return self._is_expired


class ManagedIdentityMap:
    def __init__(
        self,
        internal_type: str | None = None,
        gc_types: int | tuple[GCType] | None = None,
        gc_possibility: float | None = None,
    ):
        self._internal_type: str = internal_type
        self._gc_types: int | None = gc_types

        self._identity_map_: IdentityMap = IdentityMap()
        self._hits_misses_counter_: HitsMisses = HitsMisses()
        self._lru_list_: LRUList = LRUList()
        self._tags_manager_: TagsManager | None = None
        self._ttl_manager_: TTLManager = None
        self._gc_operator_: GCOperator = GCOperator(gc_types, gc_possibility, self.gc_run())

    @property
    def internal_type(self) -> str:
        return self._internal_type

    @property
    def _identity_map(self) -> IdentityMap:
        return self._identity_map_

    @property
    def _hits_misses_counter(self) -> HitsMisses:
        return self._hits_misses_counter_

    @property
    def _lru_list(self) -> LRUList:
        return self._lru_list_

    @property
    def _tags_manager(self) -> TagsManager:
        if self._tags_manager_ is None:
            self._tags_manager_ = TagsManager()
        return self._tags_manager_

    @property
    def _ttl_manager(self) -> TTLManager:
        if self._ttl_manager_ is None:
            self._ttl_manager_ = TTLManager()
        return self._ttl_manager_

    @property
    def _gc_operator(self) -> GCOperator:
        return self._gc_operator_

    def validate_item(self, data: Any) -> bool:
        if self.internal_type is not None:
            if not isinstance(data, self.internal_type):
                return False
        return True

    def _validate_item_or_raise(self, data: Any) -> bool:
        if not self.validate_item(data):
            raise ValueError(f"Data must be instance of {self._internal_type}")
        return True

    def has(self, key: str | int) -> bool:
        return self._identity_map.has(key)

    def get(self, key: str | int) -> Any | None:
        item = self._identity_map.get(key)
        if item is not None:
            self._hits_misses_counter.hit()
            self._lru_list.upsert(key)
            return item
        self._hits_misses_counter.miss()
        return None

    def _mark_item(self, key: str | int, is_deleted: bool = False) -> bool:
        data = self._identity_map.get(key)
        if data is None:
            return False
        try:
            if data.identity_map_info is None:
                data.identity_map_info = {}
            data.identity_map_info = IdentityMapInfo(
                is_expired=self._ttl_manager.is_expired(key), is_deleted=is_deleted, stats={}
            )
            return True
        except AttributeError:
            return False

    def _mark_item_deleted(self, key: str | int) -> bool:
        data = self._identity_map.get(key)
        if data is None:
            return False
        try:
            if data.identity_map_info is None:
                if not self._mark_item(key, is_deleted=True):
                    return False
            data.identity_map_info.is_deleted = True
            return True
        except AttributeError:
            return False

    def add(self, key: str | int, data: Any, **kwargs: Unpack[IdentityMapAddParams]) -> None:
        self._validate_item_or_raise(data)
        self._identity_map.add(key, data)
        self._mark_item(key, data)
        self._lru_list.upsert(key)
        if ttl := kwargs.get("ttl"):
            self._ttl_manager.set_ttd(key, ttl)
        if tags := kwargs.get("tags"):
            for tag in tags:
                self._tags_manager.set_tag(key, tag)

    def remove(self, key: str | int) -> None:
        self._identity_map.remove(key)
        self._lru_list.remove(key)
        self._ttl_manager.remove_ttd(key)
        self._tags_manager.remove_key(key)
        self._mark_item_deleted(key)

    def get_or_fetch(self, key: str | int, loader: Callable[[], Any], **kwargs: Unpack[IdentityMapAddParams]) -> Any:
        data = self.get(key)
        if data is not None:
            return data

        data = loader()
        self.add(key, data, **kwargs)
        return data

    def clear(self) -> None:
        self._identity_map.clear()
        self._lru_list.clear()
        self._ttl_manager.clear()
        self._tags_manager.clear()

    def gc_run(self) -> None:
        pass

    def stats(self) -> dict[str, Any] | None:
        return {
            "hits": self._hits_misses_counter.hits,
            "misses": self._hits_misses_counter.misses,
            "hit_rate": self._hits_misses_counter.get_hit_rate(),
            "miss_rate": self._hits_misses_counter.get_miss_rate(),
            "count": len(self._identity_map),
            "tags_count": len(self._tags_manager),
        }

    def __len__(self) -> int:
        return len(self._identity_map)

    def __iter__(self) -> Iterator[Any]:
        return self._identity_map.__iter__()


class IdentityMapsCollection:
    def __init__(self, gc_type: int | None = None, gc_possibility: float | None = None):
        self._maps: dict[str, ManagedIdentityMap] = {}
        self._gc = gc_type
        self._gc_possibility = gc_possibility

    def get_map(self, items_type: str) -> ManagedIdentityMap:
        if items_type not in self._maps:
            self._maps[items_type] = ManagedIdentityMap(
                internal_type=items_type, gc_types=self._gc, gc_possibility=self._gc_possibility
            )

    def run_gc(self) -> None:
        for one_map in self._maps:
            one_map.gc_run()

    def clear_map(self, items_type: str) -> None:
        if items_type in self._maps:
            self._maps[items_type].clear()

    def clear(self) -> None:
        for one_map in self._maps:
            one_map.clear()

    def hits(self) -> int:
        return sum(one_map.hits for one_map in self._maps.values())

    def misses(self) -> int:
        return sum(one_map.misses for one_map in self._maps.values())

    def stats(self) -> dict[str, Any]:
        return {
            "hits": self.hits(),
            "misses": self.misses(),
            "maps": {one_map.internal_type: one_map.stats() for one_map in self._maps.values()},
        }

    def __len__(self) -> int:
        return len(self._maps)

    def __iter__(self) -> Iterator[ManagedIdentityMap]:
        return iter(self._maps.values())
