from .env import EnvHelper, EnvValue, EnvSecretValue
from .config_helper import ConfigHelper, ConfigError

env = EnvHelper()


def env_secret(key: str, default: str | None = None) -> EnvSecretValue:
    return env(key, default, is_secret=True)
