from pathlib import Path
from typing import Any, List

import yaml


class Env:
    def __init__(self, config_path: Path | None = None):
        """Load configuration and initialize base path/mode settings.

        Args:
            config_path (Path | None): YAML containing ``base_path`` and pattern
                associations. When ``None`` the environment starts empty.

        Returns:
            None
        """
        self.sequence = -1
        self.base_path: Path = Path(".")
        self.pattern: str | None = None
        self.config: dict[str, Any] = {}
        self.assoc: dict[str, Any] = {}
        if config_path is not None:
            with open(config_path, "r", encoding="utf-8") as f:
                self.assoc = yaml.load(f, Loader=yaml.FullLoader)
                base_path_array: list[str] = self.assoc["base_path"]
                self.base_path = self.make_path(base_path_array)

    def make_path(self, path_array: list[str]) -> Path:
        """Convert a sequence of path components into a concrete path.

        Args:
            path_array (list[str]): Ordered segments such as
                ``['C:/data', 'courses']``.

        Returns:
            Path | None: Composed path or ``None`` when no components exist.
        """
        base_path = Path(".")
        if path_array is not None:
            top_dir = path_array.pop(0)
            top_path = Path(top_dir)
            base_path = top_path / Path(*path_array)

        return base_path

    def mode(self):
        """Return the scraper mode stored in the active pattern.

        Returns:
            str: Mode string, defaulting to ``"H3"`` when unspecified.
        """
        mode = self.config["mode"]
        if mode is None:
            mode = "H3"
        return mode

    def set_base_path(self, base_path: Path):
        """Persist an externally provided root directory.

        Args:
            base_path (Path): Directory serving as the root for pattern paths.

        Returns:
            None
        """
        self.base_path = base_path

    def set_pattern(self, pattern: str):
        """Load the configuration block associated with ``pattern``.

        Args:
            pattern (str): Key in ``assoc`` (e.g., ``'Udemy-2-file'``).

        Returns:
            dict | None: Selected configuration or ``None`` when unknown.
        """
        self.pattern = pattern
        if pattern not in self.assoc:
            return None
        self.config = self.assoc[pattern]
        return self.config

    def get_files(self) -> List[Path]:
        """Resolve the files or directory contents defined by the pattern.

        Returns:
            List[Path]: Concrete file paths ready for scraping.
        """
        print("env:get_files")
        if len(self.config) == 0:
            print("0 env:get_files")
            self.sequence = -1
            return []
        else:
            dir_path = self.base_path / Path(*self.config["dir"])
            print(f"2 env:get_files dir_path={dir_path}")
            self.sequence = int(dir_path.stem)

            if self.config["kind"] == "file":
                # 指定されたファイルのみを返す
                files = self.config.get("files", [])
                return [dir_path / file for file in files]
            else:
                # 指定ディレクトリの直下に存在するファイルの一覧を返す
                if not dir_path.exists() or not dir_path.is_dir():
                    return []
                files = [f for f in dir_path.iterdir() if f.is_file()]
                return sorted(files)
