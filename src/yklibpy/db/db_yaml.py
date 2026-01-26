import sys
from pathlib import Path

import yaml

from yklibpy.common.util import Util
from yklibpy.common.util_yaml import UtilYaml
from yklibpy.db.db_base import DbBase


class DbYaml(DbBase):
    def __init__(self, fname):
        DbBase.__init__(self)
        self.fname = fname
        self.fname_path = Path(fname)
        self.data = {}

    def load(self, encoding=None, tags=[]):
        Util.ensure_file_path(self.fname_path)

        if encoding is None:
            encoding = Util.detect_encoding(self.fname_path)
        if encoding is None:
            encoding = Util.get_default_encoding()

        with open(self.fname_path, "r", encoding=encoding) as f:
            # tag = "tag:yaml.org,2002:python/object:yklibpy.htmlparser.amazonsavedcartscraper.WorkInfo"
            UtilYaml._register_constructors(tags=tags)
            self.data = yaml.safe_load(f)
            if self.data is None:
                self.data = {}

        return self.data

    def save(self):
        UtilYaml.save_yaml(self.data, self.fname_path)
        return True

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        return True

    def get_item(self, key):
        return self.data[key]

    def set_item(self, key, value):
        self.data[key] = value
        return True

    def clear(self):
        self.data = {}
        return True

    def count(self):
        return len(self.data)

    def list_text(self, key):
        listx = [value[key] for value in self.data.values()]
        return listx


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("DBファイルが指定されていません")
        exit(10)
