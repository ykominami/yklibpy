from pathlib import Path
from typing import Any


class ConfigPrepare:
    """HTML パーサ関連設定の辞書アクセスを簡略化する。"""

    def __init__(self, parent_file_path: Path, assoc: dict[str, Any]) -> None:
        """親ファイル位置と設定辞書を保持する。"""
        self.parent_file_path = parent_file_path
        self.assoc = assoc

    def get(self, key: str) -> Any:
        """指定キーに対応する設定値を返す。"""
        return self.assoc[key]

    def get_command(self) -> Any:
        """`command` セクション全体を返す。"""
        return self.assoc["command"]

    def get_command_dir(self) -> Any:
        """コマンド関連ファイルの配置ディレクトリを返す。"""
        return self.assoc["command"]["dir"]

    def get_category_config_file_extname(self) -> Any:
        """カテゴリ設定ファイルの拡張子を返す。"""
        return self.assoc["category-config-file-extname"]

    def get_utility_category(self) -> Any:
        """ユーティリティカテゴリ一覧を返す。"""
        return self.assoc["command"]["utility-category"]

    def get_utility_root(self) -> Any:
        """ユーティリティ探索の起点設定を返す。"""
        return self.assoc["command"]["utility-root"]

    def get_category(self) -> Any:
        """`category` セクション全体を返す。"""
        return self.assoc["category"]

    def get_htmlparser(self) -> Any:
        """HTML パーサ用カテゴリ設定を返す。"""
        return self.assoc["category"]["htmlparser"]
