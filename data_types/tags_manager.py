from typing import List


class TagsManager:
    def __init__(self):
        self._tags: dict[str, set(str | int)] = {}
        self._key_to_tags: dict[str | int, set(str)] = {}

    @property
    def tags(self) -> set[str]:
        return set(self._tags.keys())

    @property
    def keys(self) -> set[str | int]:
        return set(self._key_to_tags.keys())

    def tag_exists(self, tag: str) -> bool:
        return tag in self._tags

    def key_exists(self, key: str | int) -> bool:
        return key in self._key_to_tags

    def set_tag(self, key: str | int, tag: str) -> None:
        if not self.tag_exists(tag):
            self._tags[tag] = set()
        self._tags[tag].add(key)
        self._key_to_tags[key] = self._key_to_tags.get(key, set())
        self._key_to_tags[key].add(tag)

    def remove_tag(self, key: str | int, tag: str, with_clean=True) -> None:
        if self.tag_exists(tag) and key in self._key_to_tags.get(key, set()):
            self._tags[tag].remove(key)
            if with_clean:
                self._key_to_tags[key].remove(tag)

    def get_tags_for_key(self, key: str | int) -> List[str]:
        return list(self._key_to_tags.get(key, set()))

    def get_keys_for_tag(self, tag: str) -> List[str]:
        return list(self._tags.get(tag, set()))

    def remove_key(self, key: str | int) -> None:
        if self.key_exists(key):
            tags = self.get_tags_for_key(key)
            for tag in tags:
                self.remove_tag(key, tag, with_clean=False)
            del self._key_to_tags[key]

    def clear(self) -> None:
        self._tags.clear()
        self._key_to_tags.clear()

    def __len__(self) -> int:
        return len(self._tags)
