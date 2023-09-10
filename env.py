import os
from dotenv import dotenv_values


class EnvValue:
    def __init__(self, value: str | None = None, name: str | None = None):
        self._value = value
        self._name = name

    @property
    def name(self) -> str:
        return self._name if self._name is not None else ""

    @property
    def value(self) -> str:
        return self._value if self._value is not None else ""

    def or_raise(self) -> str:
        if self._value is None:
            raise KeyError(f"Environment variable {self.name} not set")
        return self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'<EnvValue value="{self.value}">'

    def __len__(self):
        return len(self.value)

    def is_empty(self):
        return len(self) == 0

    def __bool__(self):
        return not self.is_empty()

    def is_none(self):
        return self._value is None

    def strict(self):
        return self._value


class EnvSecretValue(EnvValue):
    @property
    def secret(self):
        return self._value if self._value is not None else ""

    def _secret_display(self):
        return "********" if self._value is not None else ""

    @property
    def value(self):
        return self._secret_display()

    def secret_or_raise(self):
        if self._value is None:
            raise KeyError(f"Environment variable {self.name} not set")
        return self.secret

    def __len__(self):
        return len(self.secret)

    def strict(self):
        return self.value if self._value is not None else None


def load_env(with_parent: bool = True):
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.abspath(os.path.join(current_file_dir, ".env"))

    parent_values = {}
    if with_parent:
        parent_env_path = os.path.abspath(os.path.join(current_file_dir, "../.env"))
        parent_values = dotenv_values(parent_env_path)

    environment = {
        **parent_values,
        **dotenv_values(env_path),
        **os.environ,
    }

    return environment


def _env_raw(key: str, default: str | None = None) -> str | None:
    if not hasattr(_env_raw, "environment"):
        _env_raw.environment = load_env()
    if key not in _env_raw.environment:
        return default
    return _env_raw.environment[key]


def env(key: str, default: str | None = None) -> EnvValue:
    if not hasattr(env, "values"):
        env.values = {}
    if key not in env.values:
        value = _env_raw(key, default)
        env.values[key] = EnvValue(value, key)
    return env.values[key]


def env_secret(key: str, default: str | None = None) -> EnvSecretValue:
    if not hasattr(env_secret, "values"):
        env_secret.values = {}
    if key not in env_secret.values:
        value = _env_raw(key, default)
        env_secret.values[key] = EnvSecretValue(value, key)
    return env_secret.values[key]
