from yklibpy.cli.cli import Cli
from yklibpy.common.loggerx import Loggerx

__all__ = ["Cli", "xmain", "ymain"]


def xmain() -> str:
    """cli パッケージの疎通確認用メッセージを返す。"""
    Loggerx.debug("Hello from yklibpy.cli!", __name__)
    return "Hello from yklibpy.cli!"


def ymain() -> str:
    """cli パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.cli!", __name__)
    return "Y Hello from yklibpy.cli!"


if __name__ == "__main__":
    xmain()
