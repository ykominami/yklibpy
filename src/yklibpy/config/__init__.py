from yklibpy.common.loggerx import Loggerx
from yklibpy.config.appconfig import AppConfig

__all__ = ["AppConfig", "xmain", "ymain"]


def xmain() -> None:
    """config パッケージの疎通確認用メッセージを返す。"""
    Loggerx.debug("Hello from yklibpy.config!", __name__)


def ymain() -> None:
    """config パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.config!", __name__)


if __name__ == "__main__":
    xmain()
