from pathlib import Path
from typing import Any


class ConfigPrepare:
    def __init__(self, parent_file_path: Path, assoc: dict[str, Any]) -> None:
        self.parent_file_path = parent_file_path
        self.assoc = assoc

    def get(self, key: str) -> Any:
        return self.assoc[key]

    def get_command(self) -> Any:
        return self.assoc["command"]

    def get_command_dir(self) -> Any:
        return self.assoc["command"]["dir"]

    def get_category_config_file_extname(self) -> Any:
        return self.assoc["category-config-file-extname"]

    def get_utility_category(self) -> Any:
        return self.assoc["command"]["utility-category"]

    def get_utility_root(self) -> Any:
        return self.assoc["command"]["utility-root"]

    def get_category(self) -> Any:
        return self.assoc["category"]

    def get_htmlparser(self) -> Any:
        return self.assoc["category"]["htmlparser"]
