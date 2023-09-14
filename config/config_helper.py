from typing import Any
from env import EnvValue


class ConfigError(Exception):
    pass


class ConfigHelper:
    def __init__(self, config: dict[str, Any] | None = None):
        self._config = config

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    def get(self, key: str | tuple, default: Any = None, raise_exception: bool = False) -> Any:
        keys = key.split(".")

        current_value = self.config
        for k in keys:
            if isinstance(current_value, dict) and k in current_value:
                current_value = current_value[k]
            else:
                if raise_exception:
                    raise KeyError(f"Key {key} not found in config")
                return default

        if isinstance(current_value, EnvValue):
            return current_value.value
        return current_value

    def __call__(self, key: str | tuple, default: Any = None, raise_exception: bool = False) -> Any:
        return self.get(key, default, raise_exception)
