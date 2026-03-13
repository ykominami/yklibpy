import logging
from typing import ClassVar


class Loggerx:
    """ロガー生成とログレベル管理を集約する。"""

    _loggers: ClassVar[dict[str, logging.Logger]] = {}
    _log_level: ClassVar[int] = logging.INFO

    @classmethod
    def _set_log_level(cls, log_level: int = logging.INFO) -> None:
        """既定のログレベルを更新し、標準設定へ反映する。"""
        cls._log_level = log_level
        logging.basicConfig(level=cls._log_level)

    @classmethod
    def _get_or_create(cls, name: str, log_level: int = logging.INFO) -> logging.Logger:
        """名前に対応するロガーを取得し、未生成なら作成する。"""
        logger = cls._loggers.get(name, None)
        if logger is None:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger

        logger.setLevel(cls._log_level)
        return logger

    @classmethod
    def debug(cls, message: str, name: str | None = None) -> None:
        """デバッグレベルでメッセージを記録する。"""
        cls._get_or_create(name or "yklibpy", logging.DEBUG).debug(message)

    @classmethod
    def info(cls, message: str, name: str | None = None) -> None:
        """情報レベルでメッセージを記録する。"""
        cls._get_or_create(name or "yklibpy", logging.INFO).info(message)

    @classmethod
    def warning(cls, message: str, name: str | None = None) -> None:
        """警告レベルでメッセージを記録する。"""
        cls._get_or_create(name or "yklibpy", logging.WARNING).warning(message)

    @classmethod
    def error(cls, message: str, name: str | None = None) -> None:
        """エラーレベルでメッセージを記録する。"""
        # if cls._verbose:
        cls._get_or_create(name or "yklibpy", logging.ERROR).error(message)

    @classmethod
    def critical(cls, message: str, name: str | None = None) -> None:
        """致命的エラーとしてメッセージを記録する。"""
        #if cls._verbose:
        cls._get_or_create(name or "yklibpy", logging.CRITICAL).critical(message)
