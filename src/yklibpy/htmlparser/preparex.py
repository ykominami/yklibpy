import re
from pathlib import Path

from ..common.util import Util
from .configprepare import ConfigPrepare


class Preparex:
    def __init__(self, top_dir, category, config_parent_dir, assoc):
        config = ConfigPrepare(config_parent_dir, assoc)
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
        target_type = "file"
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
        """
    print(top_config.get_command())
    print(top_config.get_category())
    print(top_config.get_htmlparser())
    print(top_config.get_utility_category())
    print(top_config.get_utility_root())
    """
        """
    if parent_path.exists() and parent_path.is_dir():
        list = parent_path.rglob('*.bat')
        # list = parent_path.glob('*.bat')
        # list = parent_path.glob('*.yaml')
        # list = parent_path.rglob('*.yaml')
        # list = parent_path.rglob('*.json')
        for item in list:
            print(f'item={item.resolve()}')
    """

    def list_files_containing(self, path, search_string):
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

    def list_files(self, path, name):
        files = self.list_files_containing(path, name)
        for file in files:
            print(file)
            print(file.name)

    def list_htmlparser_files(self, name):
        files = self.list_files_containing(self.htmlparser_path, name)
        for file in files:
            print(file)
            print(file.name)
            print(file.stem)
            print(file.suffix)
            print(file.parent)

    def list_bat1_files(self, name):
        files = self.list_files_containing(self.bat1_path, name)
        for file in files:
            print(file)
            print(file.name)

    def list_utility_files(self, name, suffix):
        list = Util.list_files(name, self.parts, suffix)
        return list


if __name__ == "__main__":
    preparex = Preparex()
    name_left = "htmlparser_"
    name_right = "Amazon-KU"
    name = f"{name_left}{name_right}"
    suffix = ".bat"
    list = preparex.list_utility_files(name, suffix)
    for fx in list:
        print(f"fx={fx}")

    bat1_files = preparex.list_files_containing(preparex.bat1_path, name)
    for file in bat1_files:
        print(f"1 file={file}")
        if file is not None:
            # print(f'2 {file.name} is found')
            file_path = Path(file)
            if str(file_path.name) in list:
                print(f"file_path.name={file_path.name} found")
            else:
                print(f"file_path.name={file_path.name} not found")
