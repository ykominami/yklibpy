import os
from pathlib import Path


class FileItem:
    def __init__(self, file):
        self.file_file = file
        self.file_path = Path(file)
        self.file_type = self.get_file_type(file) if file else None

    def get_file_type(self, file_path):
        """
        引数で指定されたファイルのパスから拡張子を取り出し、大文字小文字の区別なく、
        ファイルの種別を文字列で返す。

        Args:
            file_path: ファイルパス

        Returns:
            "YAML": .yaml, .yml の場合
            "JSON": .json の場合
            "TOML": .toml の場合
            "TEXT": .txt の場合
            "OTHER": 上記以外の場合
            None: file_path が None の場合
        """
        if file_path is None:
            return None
        _, ext = os.path.splitext(file_path)
        ext_lower = ext.lower()

        if ext_lower in [".yaml", ".yml"]:
            return "YAML"
        elif ext_lower == ".json":
            return "JSON"
        elif ext_lower == ".toml":
            return "TOML"
        elif ext_lower == ".txt":
            return "TEXT"
        else:
            return "OTHER"
