from typing import Any, ClassVar


class AppConfig:
    FILE_TYPE_YAML = "YAML"
    FILE_TYPE_JSON = "JSON"
    FILE_TYPE_JSON = "JSON"

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
    }

    directory_assoc: ClassVar[dict[str, dict[str, dict[str, Any]]]] = {
        KIND_DB: {
            BASE_NAME_CONFIG: {
                PATH: {},
            }
        }
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
