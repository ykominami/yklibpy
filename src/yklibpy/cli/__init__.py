from yklibpy.cli.cli import Cli
from yklibpy.common.loggerx import Loggerx

__all__ = ["Cli", "xmain", "ymain"]


def xmain() -> None:
    """cli パッケージの疎通確認用メッセージを出力する。"""
    msg = "Hello from yklibpy.cli!"
    Loggerx.debug(msg, __name__)
    print(msg)


def ymain() -> None:
    """cli パッケージ of 別系統の疎通確認用メッセージを出力する。"""
    msg = "Y Hello from yklibpy.cli!"
    Loggerx.debug(msg, __name__)
    print(msg)


if __name__ == "__main__":
    xmain()
