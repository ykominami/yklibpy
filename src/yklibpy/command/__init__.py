from yklibpy.command.command import Command
from yklibpy.command.command_gh_user import CommandGhUser
from yklibpy.command.fetchcount import FetchCount
from yklibpy.common.loggerx import Loggerx

__all__ = ["Command", "CommandGhUser", "FetchCount", "xmain", "ymain"]


def xmain() -> str:
    """command パッケージの疎通確認用メッセージを返す。"""
    Loggerx.debug("Hello from yklibpy.command!", __name__)
    return "Hello from yklibpy.command!"


def ymain() -> str:
    """command パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.command!", __name__)
    return "Y Hello from yklibpy.command!"


if __name__ == "__main__":
    xmain()
