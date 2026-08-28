from __future__ import annotations

import argparse


class Cli:
    """`argparse.ArgumentParser` を扱いやすく包む。"""

    def __init__(self, help_text: str) -> None:
        """説明文付きのパーサを初期化する。"""
        self.parser = argparse.ArgumentParser(
            description=help_text
        )
        self.args: argparse.Namespace | None = None

    def get_parser(self) -> argparse.ArgumentParser:
        """保持している引数パーサを返す。"""
        return self.parser

    def get_args(self) -> argparse.Namespace | None:
        """直近に解析した引数結果を返す。"""
        return self.args

    def parse_args(self) -> argparse.Namespace:
        """コマンドライン引数を解析して保持する。"""
        self.args = self.parser.parse_args()
        return self.args

    def get_subparsers(self, name: str) -> argparse._SubParsersAction[argparse.ArgumentParser]:
        """指定名を `dest` に持つサブコマンド定義を作成する。"""
        self.subparsers = self.parser.add_subparsers(dest=name, required=True)
        return self.subparsers
