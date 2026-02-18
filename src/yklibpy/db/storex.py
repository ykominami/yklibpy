import json
from pathlib import Path
from typing import Any

import yaml

from yklibpy.config.appconfig import AppConfig


class Storex:
    _file_type_dict: dict[str, str] = {}

    @classmethod
    def set_file_type_dict(cls, file_type_dict: dict[str, str]) -> None:
        cls._file_type_dict = file_type_dict

    @classmethod
    def get_ext_name(cls, file_type: str) -> str:
        return cls._file_type_dict[file_type]

    def __init__(self, file_type: str, file_name_array: list[str]):
        self.file_name_array = file_name_array
        self.file_type = file_type

        # file_name_arrayは完全なパス要素の配列（呼び出し元で構築済み）
        top_dir = file_name_array.pop(0)
        top_path = Path(top_dir)
        for file_name in file_name_array:
            # print(f'file_name={file_name}')
            top_path = top_path / Path(file_name)

        self.file_path = top_path
        # self.file_path = Path(**file_name_array)
        self.store: dict[str, Any] = {}

    def get_value(self, key: str) -> Any:
        return self.store.get(key)

    def get_store(self) -> dict[str, Any]:
        return self.store

    def load(self) -> dict[str, Any]:
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                if self.file_type == AppConfig.FILE_TYPE_YAML:
                    self.store = yaml.safe_load(f) or {}
                elif self.file_type == AppConfig.FILE_TYPE_JSON:
                    self.store = json.load(f)
                else:
                    self.store = {"_lines": f.readlines()}

        return self.store

    def output(self, data: Any) -> None:
        # 親ディレクトリが存在しない場合は作成
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            if self.file_type == AppConfig.FILE_TYPE_YAML:
                yaml.dump(data, f, allow_unicode=True)
            elif self.file_type == AppConfig.FILE_TYPE_JSON:
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                f.write(str(data))
