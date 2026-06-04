from yklibpy.common.loggerx import Loggerx
from yklibpy.config.appconfig import AppConfig

__all__ = ["AppConfig", "xmain", "ymain"]


def xmain() -> str:
    """config パッケージの疎通確認用メッセージを返す。"""
    Loggerx.debug("Hello from yklibpy.config!", __name__)
    return "Hello from yklibpy.config!"


def ymain() -> str:
    """config パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.config!", __name__)
    return "Y Hello from yklibpy.config!"


if __name__ == "__main__":
    xmain()
