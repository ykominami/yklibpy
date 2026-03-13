from pathlib import Path
from typing import Any, cast

import yaml

from yklibpy.common.loggerx import Loggerx


class Env:
    """設定ファイルからスクレイピング対象の環境情報を組み立てる。"""

    def __init__(self, config_path: Path | None = None) -> None:
        """設定パスを読み込み、基準パスとパターン情報を初期化する。"""
        self.sequence = -1
        self.base_path: Path = Path(".")
        self.pattern: str | None = None
        self.config: dict[str, Any] = {}
        self.assoc: dict[str, Any] = {}
        if config_path is not None:
            with open(config_path, "r", encoding="utf-8") as f:
                self.assoc = yaml.load(f, Loader=yaml.FullLoader)
                base_path_array = cast(list[str], self.assoc["base_path"])
                self.base_path = self.make_path(base_path_array)

    def make_path(self, path_array: list[str]) -> Path:
        """パス要素の配列から実際の `Path` を組み立てる。"""
        base_path = Path(".")
        top_dir = path_array.pop(0)
        top_path = Path(top_dir)
        base_path = top_path / Path(*path_array)

        return base_path

    def mode(self) -> str:
        """現在の設定に対応するスクレイパーモードを返す。"""
        mode = cast(str | None, self.config.get("mode"))
        if mode is None:
            return "H3"
        return mode

    def set_base_path(self, base_path: Path) -> None:
        """探索基準となるベースパスを設定する。"""
        self.base_path = base_path

    def set_pattern(self, pattern: str) -> dict[str, Any] | None:
        """指定パターンに対応する設定ブロックを選択する。"""
        self.pattern = pattern
        if pattern not in self.assoc:
            return None
        self.config = self.assoc[pattern]
        return self.config

    def get_files(self) -> list[Path]:
        """現在の設定から処理対象ファイル一覧を解決する。"""
        Loggerx.error(f"env:get_files self.config={self.config}", __name__)
        if len(self.config) == 0:
            Loggerx.error("0 env:get_files", __name__)
            self.sequence = -1
            return []
        else:
            dir_parts = cast(list[str], self.config["dir"])
            dir_path = self.base_path / Path(*dir_parts)
            Loggerx.error(f"2 env:get_files dir_path={dir_path}", __name__)
            self.sequence = int(dir_path.stem)

            if self.config["kind"] == "file":
                # 指定されたファイルのみを返す
                files_raw = cast(list[Any], self.config.get("files", []))
                return [dir_path / str(file) for file in files_raw]
            else:
                # 指定ディレクトリの直下に存在するファイルの一覧を返す
                if not dir_path.exists() or not dir_path.is_dir():
                    return []
                files = [f for f in dir_path.iterdir() if f.is_file()]
                return sorted(files)
