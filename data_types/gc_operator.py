import enum
import random
from typing import Callable


@enum.unique
class GCType(enum.IntEnum):
    TTL = 1
    LRU = 2
    LFRU = 4

    ALL = 7

    def __str__(self):
        return str(self.value)


class GCOperator:
    def __init__(self, gc_types: int | tuple[GCType] = None, possibility: float = 0.5, func: Callable | None = None):
        if gc_types is None:
            self._gc_types = tuple()
        elif isinstance(gc_types, int):
            self._gc_types = self.to_gc_types(gc_types)
        elif isinstance(gc_types, tuple):
            self._gc_types = self.validate_gc_types(gc_types)
        else:
            raise TypeError(f"gc_types must be of type int or tuple, not {type(gc_types)}")

        self._func: Callable | None = func

        self.possibility: float = possibility

    @property
    def gc_types(self) -> tuple[GCType]:
        return self._gc_types

    @property
    def func(self) -> Callable | None:
        return self._func

    def validate_gc_types(self, gc_types: tuple[GCType]) -> tuple[GCType]:
        for gc_type in gc_types:
            if not isinstance(gc_type, GCType):
                raise TypeError(f"gc_type must be of type GCType, not {type(gc_type)}")
        return gc_types

    def to_gc_types(self, gc_types: int) -> tuple[GCType]:
        return tuple(flag for flag in GCType if flag & gc_types)

    def in_gc(self, gc_type: GCType) -> bool:
        return gc_type in self.gc_types

    def __int__(self) -> int:
        return sum(gc_type.value for gc_type in self.gc_types)

    def __iter__(self):
        yield from self.gc_types

    def is_possible(self) -> tuple[GCType]:
        return random.random() < self.possibility

    def run(self) -> None:
        if self.func is not None:
            if self.is_possible():
                if callable(self.func):
                    self.func()  # pylint: disable=E1102
