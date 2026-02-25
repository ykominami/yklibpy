import logging


class Loggerx:
    _loggers: dict[str, logging.Logger] = {}
    _log_level: int = logging.INFO

    @classmethod
    def _set_log_level(cls, log_level: int = logging.INFO) -> logging.Logger:
        cls._log_level = log_level
        logging.basicConfig(level=cls._log_level)
        return cls._log_level

    @classmethod
    def _get_or_create(cls, name: str, log_level: int = logging.INFO) -> logging.Logger:
        logger = cls._loggers.get(name, None)
        if logger is None:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger

        return logger

    @classmethod
    def debug(cls, message: str, name: str) -> None:
        cls._get_or_create(name, logging.DEBUG).debug(message)

    @classmethod
    def info(cls, message: str, name: str) -> None:
        cls._get_or_create(name, logging.INFO).info(message)

    @classmethod
    def warning(cls, message: str, name: str) -> None:
        cls._get_or_create(name, logging.WARNING).warning(message)

    @classmethod
    def error(cls, message: str, name: str) -> None:
        # if cls._verbose:
        cls._get_or_create(name, logging.ERROR).error(message)

    @classmethod
    def critical(cls, message: str, name: str) -> None:
        #if cls._verbose:
        cls._get_or_create(name, logging.CRITICAL).critical(message)
