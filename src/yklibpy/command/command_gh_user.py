from yklibpy.command.command import Command
from yklibpy.common.util import Util


class CommandGhUser(Command):
    DEFAULT_VALUE_USER = None

    def __init__(self) -> None:
        pass

    def run(self) -> str:
        command_line = 'gh api user --jq ".login"'
        output = self.run_command_simple(command_line)
        user = Util.normalize_string(output)
        return user or ""
