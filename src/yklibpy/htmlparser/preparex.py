import re
from pathlib import Path
from typing import List, Literal

from yklibpy.common.util import Util
from yklibpy.htmlparser.configprepare import ConfigPrepare


class Preparex:
    def __init__(
        self, top_dir: str, category: str, config_parent_dir: str, assoc: dict
    ):
        config = ConfigPrepare(Path(config_parent_dir), assoc)
        self.parts = config.get_utility_category()
        self.top_path = Path(top_dir)
        self.bat1_path = self.top_path / config.get_command_dir()
        self.htmlparser_path = self.top_path / category

        self.htmlparser_path.mkdir(parents=True, exist_ok=True)

        self.bat1_path.mkdir(parents=True, exist_ok=True)
        self.htmlparser_path.mkdir(parents=True, exist_ok=True)

        ul = Util.UniqueList()
        file_extname = config.get_category_config_file_extname()
        # file_extname_x = rf"file_extname{'$'}"
        # re_file_extname = re.compile(re.escape(file_extname_x))
        file_extname_escape = re.escape(file_extname)
        file_extname_x = file_extname_escape + "$"
        # OK file_extname_r = r"\.yaml$"
        # re_file_extname = re.compile(re.escape(file_extname_r))
        # re_file_extname = re.compile(file_extname_r)
        re_file_extname = re.compile(file_extname_x)
        pattern = "*"
        # pattern = ".yaml"
        print(f"file_extname={file_extname}")
        print(f"self.top_path={self.top_path}")
        target_type: Literal["file", "dir", "both"] = "file"
        # target_type = "dir"
        # target_type = "both"
        for path in Util.find_paths(self.top_path, pattern, target_type):
            # print(f'path={path}')
            name = str(path.name)
            # print(f'0 name={name}')
            if not re_file_extname.search(name):
                continue
            # print(f'1 name={name}')
            stem = path.stem

            array = stem.split("-")
            size = len(array)
            # print(f'size={size}')
            if size == 2:
                left = array[0]
                ul.append(left)
                right = array[1]

                print(f"stem={stem}")
                print(f"left={left}")
                print(f"right={right}")

        print(ul)

    def list_files_containing(self, path: Path, search_string: str) -> List[Path]:
        """
        指定パス直下に存在するファイルのうち、ファイル名が指定文字列を含むものをすべて列挙する

        Args:
          path: 検索対象のパス（Pathオブジェクトまたは文字列）
          search_string: ファイル名に含まれる文字列

        Returns:
          条件に一致するファイルのPathオブジェクトのリスト
        """
        target_path = Path(path) if isinstance(path, str) else path
        if not target_path.exists() or not target_path.is_dir():
            return []

        matching_files = []
        for file_path in target_path.iterdir():
            if file_path.is_file() and search_string in file_path.name:
                matching_files.append(file_path)

        return matching_files

    def list_files(self, path: Path, name: str) -> List[Path]:
        files = self.list_files_containing(path, name)
        for file in files:
            print(file)
            print(file.name)
        return files

    def list_htmlparser_files(self, name: str) -> List[Path]:
        files = self.list_files_containing(self.htmlparser_path, name)
        for file in files:
            print(file)
            print(file.name)
            print(file.stem)
            print(file.suffix)
            print(file.parent)
        return files

    def list_bat1_files(self, name: str) -> List[Path]:
        files = self.list_files_containing(self.bat1_path, name)
        for file in files:
            print(file)
            print(file.name)
        return files

    def list_utility_files(self, name: str, suffix: str) -> List[Path]:
        list = Util.list_files(name, self.parts, suffix)
        return list
