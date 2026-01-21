import json


class UtilJson:
    @classmethod
    def load_file(cls, file_name: str):
        data = None
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def load_string(cls, string: str):
        data = None
        data = json.loads(string)
        return data
