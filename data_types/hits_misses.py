class HitsMisses:
    def __init__(self):
        self._hits = 0
        self._misses = 0

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    def hit(self) -> None:
        self._hits += 1

    def miss(self) -> None:
        self._misses += 1

    def get_hit_rate(self) -> float:
        if self._hits == 0:
            return 0
        return self._hits / (self._hits + self._misses)

    def get_miss_rate(self) -> float:
        if self._misses == 0:
            return 0
        return self._misses / (self._hits + self._misses)

    def clear_hit_miss_rate(self) -> None:
        self._hits = 0
        self._misses = 0

    def metrics(self) -> dict:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self.get_hit_rate(),
            "miss_rate": self.get_miss_rate(),
        }
