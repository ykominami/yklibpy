import json
from typing import Any


class UtilJson:
    @classmethod
    def load_file(cls, file_name: str) -> Any:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def load_string(cls, string: str) -> Any:
        return json.loads(string)
