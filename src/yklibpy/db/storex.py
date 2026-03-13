import json
from pathlib import Path
from typing import Any, ClassVar

import toml
import yaml

from yklibpy.common.loggerx import Loggerx
from yklibpy.config.appconfig import AppConfig


class Storex:
    """ファイル種別に応じた読み書きを抽象化するストレージラッパー。"""

    _file_type_dict: ClassVar[dict[str, str]] = {}

    @classmethod
    def set_file_type_dict(cls, file_type_dict: dict[str, str]) -> None:
        """拡張子解決に使うファイル種別辞書を設定する。"""
        cls._file_type_dict = file_type_dict

    @classmethod
    def get_ext_name(cls, file_type: str) -> str:
        """ファイル種別に対応する拡張子を返す。"""
        return cls._file_type_dict[file_type]

    def __init__(
        self,
        file_type: str,
        file_name_array: list[Path] | list[str],
        data: Any = None,
    ) -> None:
        """パス要素列から保存先パスを構築し、内部データを初期化する。"""
        self.file_type = file_type
        self.file_name_array = file_name_array
        # file_name_arrayは完全なパス要素の配列（呼び出し元で構築済み）
        top_dir = file_name_array.pop(0)
        top_path = Path(top_dir)
        for file_name in file_name_array:
            Loggerx.debug(f'1 Storex.file_name_array: file_name={file_name}', __name__)
            top_path = top_path / Path(file_name)

        self.file_path = top_path
        self.store: Any = {} if data is None else data

    def set_data(self, data: Any) -> None:
        """内部に保持するデータを置き換える。"""
        self.store = data

    def get_value(self, key: str) -> Any:
        """保持データからキーに対応する値を返す。"""
        return self.store.get(key)

    def get_store(self) -> Any:
        """内部に保持しているデータ全体を返す。"""
        return self.store

    def load(self) -> Any:
        """保存先ファイルを読み込み、ファイル種別に応じて復元する。"""
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                if self.file_type == AppConfig.FILE_TYPE_YAML:
                    self.store = yaml.safe_load(f) or {}
                elif self.file_type == AppConfig.FILE_TYPE_JSON:
                    self.store = json.load(f)
                elif self.file_type == AppConfig.FILE_TYPE_TOML:
                    self.store = toml.load(f)
                else:
                    self.store = {"_lines": f.readlines()}

        return self.store

    def output(self, data: Any = None) -> None:
        """保持データまたは指定データをファイルへ書き出す。"""
        if data is None:
            data = self.store
        # 親ディレクトリが存在しない場合は作成
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        Loggerx.debug(f'1 Storex.output: self.file_path={self.file_path}', __name__)
        with open(self.file_path, "w", encoding="utf-8") as f:
            if self.file_type == AppConfig.FILE_TYPE_YAML:
                yaml.dump(data, f, allow_unicode=True)
            elif self.file_type == AppConfig.FILE_TYPE_JSON:
                json.dump(data, f, ensure_ascii=False, indent=2)
            elif self.file_type == AppConfig.FILE_TYPE_TOML:
                toml.dump(data, f)
            else:
                f.write(str(data))

    def get_name(self) -> str:
        """保存先ファイル名だけを返す。"""
        return self.file_path.name

    def get_path(self) -> Path:
        """保存先の完全パスを返す。"""
        return self.file_path