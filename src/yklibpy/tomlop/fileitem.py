from pathlib import Path
from typing import Any

from yklibpy.config.appconfig import AppConfig
from yklibpy.db.storex import Storex


class FileItem:
    """ファイルパスと `Storex` を束ねる薄いラッパー。"""

    @classmethod
    def setup(cls, file_type_dict: dict[str, str] = AppConfig.file_type_dict) -> None:
        """`Storex` で使うファイル種別定義を初期化する。"""
        Storex.set_file_type_dict(file_type_dict)

    def __init__(
        self,
        file: str | Path | list[str] | list[Path],
        data: Any = None,
    ) -> None:
        """入力値からファイルパスを確定し、対応する `Storex` を作る。"""
        if isinstance(file, list):
            filex = file.pop(0)
            if isinstance(filex, str):
                self.file_path = Path(filex)
            else:
                self.file_path = filex
                for file_name in file:
                    self.file_path = self.file_path / Path(file_name)
        else:
            self.file_path = Path(file)

        file_type = AppConfig.get_file_type(str(self.file_path))
        if file_type is None:
            raise ValueError(f"Unsupported file type: {self.file_path}")
        self.file_type = file_type
        self.storex = Storex(self.file_type, [self.file_path], data)
            
    def get_file_type(self, file_path: str | Path | None) -> str | None:
        """パスから判定したファイル種別を返す。"""
        return AppConfig.get_file_type(str(file_path) if file_path is not None else None)

    def set_data(self, data: dict[str, Any]) -> None:
        """内部 `Storex` に保持するデータを更新する。"""
        self.storex.set_data(data)

    def output(self, data: Any = None) -> None:
        """データを現在のファイルパスへ出力する。"""
        self.storex.output(data)

    def get_name(self) -> str:
        """ファイル名だけを返す。"""
        return self.storex.get_name()

    def get_path(self) -> Path:
        """ファイルの完全パスを返す。"""
        return self.storex.get_path()

    def with_suffix(self, suffix: str) -> Path:
        """同じパスに別拡張子を付けた `Path` を返す。"""
        return self.file_path.with_suffix(suffix)