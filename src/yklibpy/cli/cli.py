import argparse


class Cli:
    def __init__(self, help_text: str) -> None:
        self.parser = argparse.ArgumentParser(
            description=help_text
        )
        self.args: argparse.Namespace | None = None

    def get_parser(self) -> argparse.ArgumentParser:
        return self.parser

    def get_args(self) -> argparse.Namespace | None:
        return self.args

    def parse_args(self) -> argparse.Namespace:
        self.args = self.parser.parse_args()
        return self.args

    def get_subparsers(self, name: str) -> argparse._SubParsersAction[argparse.ArgumentParser]:
        self.subparsers = self.parser.add_subparsers(dest=name, required=True)
        return self.subparsers
