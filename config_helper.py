from typing import Any


class ConfigError(Exception):
    pass


class ConfigHelper:
    def __init__(self, config: dict[str, Any] | None = None):
        self._config = config

    @property
    def config(self) -> dict[str, Any]:
        return self._config

    @config.setter
    def config(self, config: dict[str, Any]) -> None:
        if self._config is not None:
            raise ConfigError("Config already set")
        self._config = config

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
        return current_value

    def __call__(self, key: str | tuple, default: Any = None, raise_exception: bool = False) -> Any:
        return self.get(key, default, raise_exception)


def _get_config_helper() -> ConfigHelper:
    if not hasattr(_get_config_helper, "config_helper"):
        _get_config_helper.config_helper = ConfigHelper()
    return _get_config_helper.config_helper


def load_config(config_data: dict[str, Any]) -> None:
    config_helper = _get_config_helper()
    config_helper.config = config_data


def is_config_loaded() -> bool:
    return _get_config_helper().config is not None


def get_config(key: str | tuple, default: Any = None, raise_exception: bool = False) -> Any:
    return _get_config_helper().get(key, default, raise_exception)


if __name__ == "__main__":
    print("Please use this module as a library")
