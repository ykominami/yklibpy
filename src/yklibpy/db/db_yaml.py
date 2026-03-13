import sys
from pathlib import Path
from typing import Any, cast

import yaml

from yklibpy.common.util import Util
from yklibpy.common.util_yaml import UtilYaml
from yklibpy.db.db_base import DbBase


class DbYaml(DbBase):
    """YAML ファイルを永続化先とする簡易 DB 実装。"""

    def __init__(self, fname: str) -> None:
        """対象ファイルパスと空データを初期化する。"""
        super().__init__()
        self.fname = fname
        self.fname_path = Path(fname)
        self.data: dict[str, Any] = {}

    def load(self, encoding: str | None = None, tags: list[str] | None = None) -> dict[str, Any]:
        """YAML ファイルを読み込み、辞書データとして保持する。"""
        Util.ensure_file_path(self.fname_path)

        if encoding is None:
            try:
                encoding = Util.detect_encoding(self.fname_path)
            except Exception as e:
                Loggerx.error(f"An error occurred: {e}", __name__)
                Loggerx.error(f"Encoding detection failed for file: {self.fname_path}", __name__)
                return {}
        if encoding is None:
            encoding = Util.get_default_encoding()

        with open(self.fname_path, "r", encoding=encoding) as f:
            # tag = "tag:yaml.org,2002:python/object:yklibpy.htmlparser.amazonsavedcartscraper.WorkInfo"
            tag_list = tags or []
            UtilYaml._register_constructors(tags=tag_list)
            loaded = yaml.safe_load(f)
            self.data = cast(dict[str, Any], loaded or {})

        return self.data

    def save(self) -> bool:
        """保持中の辞書を YAML ファイルへ保存する。"""
        UtilYaml.save_yaml(self.data, self.fname_path)
        return True

    def get_data(self) -> dict[str, Any]:
        """保持している全データを返す。"""
        return self.data

    def set_data(self, data: dict[str, Any]) -> bool:
        """内部データを丸ごと置き換える。"""
        self.data = data
        return True

    def get_item(self, key: str) -> Any:
        """指定キーの値を返す。存在しない場合は失敗する。"""
        return self.data[key]

    def set_item(self, key: str, value: Any) -> bool:
        """指定キーへ値を設定する。"""
        self.data[key] = value
        return True

    def clear(self) -> bool:
        """保持しているデータを空にする。"""
        self.data = {}
        return True

    def count(self) -> int:
        """保持しているキー数を返す。"""
        return len(self.data)

    def list_text(self, key: str) -> list[Any]:
        """各要素から指定キーの値だけを抽出して返す。"""
        return [cast(dict[str, Any], value)[key] for value in self.data.values()]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("DBファイルが指定されていません")
        raise SystemExit(10)
