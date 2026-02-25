import re
from pathlib import Path
from typing import List, Literal

from yklibpy.common.loggerx import Loggerx
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
        Loggerx.debug(f"1 Preparex.file_extname={file_extname}", __name__)
        Loggerx.debug(f"2 Preparex.self.top_path={self.top_path}", __name__)
        target_type: Literal["file", "dir", "both"] = "file"
        # target_type = "dir"
        # target_type = "both"
        for path in Util.find_paths(self.top_path, pattern, target_type):
            Loggerx.debug(f'3 Preparex.path={path}', __name__)
            name = str(path.name)
            Loggerx.debug(f'0 Preparex.name={name}', __name__)
            if not re_file_extname.search(name):
                continue
            Loggerx.debug(f'1 Preparex.name={name}', __name__)
            stem = path.stem

            array = stem.split("-")
            size = len(array)
            Loggerx.debug(f'4 Preparex.size={size}', __name__)
            if size == 2:
                left = array[0]
                ul.append(left)
                right = array[1]

                Loggerx.debug(f"5 Preparex.stem={stem}", __name__)
                Loggerx.debug(f"6 Preparex.left={left}", __name__)
                Loggerx.debug(f"7 Preparex.right={right}", __name__)

        Loggerx.debug(f"8 Preparex.ul={ul}", __name__)

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
            Loggerx.debug(f'1 Preparex.list_files: file={file}', __name__)
            Loggerx.debug(f'2 Preparex.list_files: file.name={file.name}', __name__)
        return files

    def list_htmlparser_files(self, name: str) -> List[Path]:
        files = self.list_files_containing(self.htmlparser_path, name)
        for file in files:
            Loggerx.debug(f'3 Preparex.list_files: file={file}', __name__)
            Loggerx.debug(f'4 Preparex.list_files: file.name={file.name}', __name__)
            Loggerx.debug(f'5 Preparex.list_files: file.stem={file.stem}', __name__)
            Loggerx.debug(f'6 Preparex.list_files: file.suffix={file.suffix}', __name__)
            Loggerx.debug(f'7 Preparex.list_files: file.parent={file.parent}', __name__)
        return files

    def list_bat1_files(self, name: str) -> List[Path]:
        files = self.list_files_containing(self.bat1_path, name)
        for file in files:
            Loggerx.debug(f'8 Preparex.list_bat1_files: file={file}', __name__)
            Loggerx.debug(f'9 Preparex.list_bat1_files: file.name={file.name}', __name__)

        return files

    def list_utility_files(self, name: str, suffix: str) -> List[Path]:
        list = Util.list_files(name, self.parts, suffix)
        return list
