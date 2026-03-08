import os
from typing import Any, ClassVar

from yklibpy.common.util import Util


class AppConfig:
    FILE_TYPE_YAML = "YAML"
    FILE_TYPE_JSON = "JSON"
    FILE_TYPE_TOML = "TOML"

    DIR_TYPE = "DIRECTORY"

    KIND_CONFIG = "config"
    KIND_DB = "db"
    KIND_FETCH = "fetch"

    BASE_NAME_CONFIG = "config"
    BASE_NAME_DB = "db"
    BASE_NAME_FETCH = "fetch"

    PATH = "path"
    FILE_TYPE = "file_type"
    EXT_NAME = "ext_name"
    VALUE = "value"
    DATE = "date"
    
    file_type_dict: ClassVar[dict[str, str]] = {
        FILE_TYPE_YAML: ".yml",
        FILE_TYPE_JSON: ".json",
        FILE_TYPE_TOML: ".toml",
    }
    file_type_reverse_dict: ClassVar[dict[str, str]] = Util.swap_dict(file_type_dict)

    file_synonym_dict: ClassVar[dict[str, str]] = {
        ".yaml": ".yml",
    }
    # クラスAppConfigを継承したクラスで拡張するときのためにエントリの身を用意しておく
    directory_assoc: ClassVar[dict[str, dict[str, dict[str, Any]]]] = {
        KIND_CONFIG: {},
        KIND_DB: {}
    }

    file_assoc: ClassVar[dict[str, dict[str, dict[str, Any]]]] = {
        KIND_CONFIG: {
            BASE_NAME_CONFIG: {
                FILE_TYPE: FILE_TYPE_YAML,
                EXT_NAME: "",
                PATH: {},
                VALUE: {},
            }
        },
        KIND_DB: {
            BASE_NAME_DB: {
                FILE_TYPE: FILE_TYPE_YAML,
                EXT_NAME: "",
                PATH: {},
                VALUE: {},
            },
            BASE_NAME_FETCH: {
                FILE_TYPE: FILE_TYPE_YAML,
                EXT_NAME: "",
                PATH: {},
                VALUE: {},
            },
        },
    }
    fetch_item: ClassVar[dict[str, str]] = {
        DATE: "",
    }

    @classmethod
    def get_file_type(cls, file_path: str | None) -> str | None:
        if file_path is None:
            return None
        _, ext = os.path.splitext(file_path)
        ext_lower = ext.lower()
        if ext_lower in cls.file_synonym_dict:
            ext_lower = cls.file_synonym_dict[ext_lower]

        file_type = cls.file_type_reverse_dict.get(ext_lower, None)
        if file_type is not None:
            return file_type

        return None