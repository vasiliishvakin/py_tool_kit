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
    def __init__(self, value: str | EnvValue | None = None, name: str | None = None):
        if isinstance(value, EnvValue):
            value = str(value)
        super().__init__(value, name)

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


class EnvHelper:
    def __init__(self, with_parent: bool = True) -> None:
        self._environment = self._load_env(with_parent)
        self._values = {}
        self._secrets = {}

    @property
    def values(self):
        return self._values

    def _load_env(self, with_parent: bool = True):
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

    def get_raw(self, key: str, default: str | None = None) -> str | None:
        if key not in self._environment:
            return default
        return self._environment[key]

    def get(self, key: str, default: str | None = None) -> EnvValue:
        if key not in self.values:
            value = self.get_raw(key, default)
            self.values[key] = EnvValue(value, key)
        return self.values[key]

    def get_secret(self, key: str, default: str | None = None) -> EnvSecretValue:
        if key not in self._secrets:
            value = self.get(key, default)
            self._secrets[key] = EnvSecretValue(value, key)
        return self._secrets[key]

    def __call__(self, key: str, default: str | None = None, is_secret=False) -> EnvValue | EnvSecretValue:
        if is_secret:
            return self.get_secret(key, default)
        return self.get(key, default)
