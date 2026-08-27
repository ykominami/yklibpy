from yklibpy.command.command import Command
from yklibpy.common.util import Util


class CommandGhUser(Command):
    """GitHub CLI からログインユーザー名を取得する。"""

    def __init__(self) -> None:
        """親クラス互換の空初期化を行う。"""
        pass

    def run(self) -> str:
        """`gh api user` を実行してユーザー名を返す。"""
        command_line = 'gh api user --jq ".login"'
        output = self.run_command_simple(command_line)
        user = Util.normalize_string(output)
        return user or ""
