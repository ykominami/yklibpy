import json
from typing import Any


class UtilJson:
    """JSON の読み込み処理をまとめた補助クラス。"""

    @classmethod
    def load_file(cls, file_name: str) -> Any:
        """JSON ファイルを読み込み、パース結果を返す。"""
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def load_string(cls, string: str) -> Any:
        """JSON 文字列をパースして Python オブジェクトへ変換する。"""
        return json.loads(string)
