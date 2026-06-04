from yklibpy.command.command import Command
from yklibpy.command.command_gh_user import CommandGhUser
from yklibpy.command.fetchcount import FetchCount
from yklibpy.common.loggerx import Loggerx

__all__ = ["Command", "CommandGhUser", "FetchCount", "xmain", "ymain"]


def xmain() -> None:
    """command パッケージの疎通確認用メッセージを出力する。"""
    msg = "Hello from yklibpy.command!"
    Loggerx.debug(msg, __name__)
    print(msg)


def ymain() -> None:
    """command パッケージの別系統の疎通確認用メッセージを出力する。"""
    msg = "Y Hello from yklibpy.command!"
    Loggerx.debug(msg, __name__)
    print(msg)


if __name__ == "__main__":
    xmain()
