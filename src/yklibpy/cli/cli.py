import argparse
from typing import Any

from yklibpy.db.appstore import AppStore

class Cli:
    def __init__(self, help_text: str) -> None:
        self.parser = argparse.ArgumentParser(
            description=help_text
        )

    def get_args(self) -> argparse.Namespace:
        return self.args

    def parse_args(self):
        self.args = self.parser.parse_args()
        return self.args

    def get_subparsers(self) -> argparse.ArgumentParser:
        return self.subparsers
