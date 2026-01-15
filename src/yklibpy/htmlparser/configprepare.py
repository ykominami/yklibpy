from pathlib import Path


class ConfigPrepare:
    def __init__(self, parent_file_path: Path, assoc: dict):
        self.parent_file_path = parent_file_path
        self.assoc = assoc

    def get(self, key):
        return self.assoc[key]

    def get_command(self):
        return self.assoc["command"]

    def get_command_dir(self):
        return self.assoc["command"]["dir"]

    def get_category_config_file_extname(self):
        return self.assoc["category-config-file-extname"]

    def get_utility_category(self):
        return self.assoc["command"]["utility-category"]

    def get_utility_root(self):
        return self.assoc["command"]["utility-root"]

    def get_category(self):
        return self.assoc["category"]

    def get_htmlparser(self):
        return self.assoc["category"]["htmlparser"]
