class SimpleIDGenerator:
    def __init__(self) -> None:
        self._last = 0
        self._free = set()

    @property
    def last(self) -> int:
        return self._last

    @property
    def next(self) -> int:
        if len(self._free) > 0:
            if len(self._free) >= self._last:
                self.reset()
            else:
                return self._free.pop()
        self._last += 1
        return self._last

    def reset(self) -> None:
        self._last = 0
        self._free.clear()

    def free(self, id: int) -> None:
        if id > self._last:
            return
        elif id == self._last:
            self._last -= 1
            return
        self._free.add(id)

    def __len__(self) -> int:
        return self._last - len(self._free)

    def __call__(self) -> int:
        return self.next()
