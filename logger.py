import logging
import logging.config


class Logger:
    def __init__(self, config: dict) -> None:
        self.configure(config)
        self._loggers = {}

    def configure(self, config: dict) -> None:
        logging.config.dictConfig(config)

    def get(self, name: str) -> logging.Logger:
        if name == "":
            name = "root"

        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)

        return self._loggers[name]

    def __call__(self, name: str) -> logging.Logger:
        return self.get(name)

    def keys(self):
        return self._loggers.keys()

    def __iter__(self):
        return iter(self._loggers)

    def add_null_handler(self, name: str) -> None:
        self.get(name).addHandler(logging.NullHandler())
