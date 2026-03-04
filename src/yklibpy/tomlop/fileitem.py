from pathlib import Path
from typing import Any

from yklibpy.config.appconfig import AppConfig
from yklibpy.db.storex import Storex


class FileItem:
    @classmethod
    def setup(cls, file_type_dict: dict[str, str] = AppConfig.file_type_dict) -> None:
        Storex.set_file_type_dict(file_type_dict)

    def __init__(
        self,
        file: str | Path | list[str] | list[Path],
        data: Any = None,
    ) -> None:
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
        return AppConfig.get_file_type(str(file_path) if file_path is not None else None)

    def set_data(self, data: dict[str, Any]) -> None:
        self.storex.set_data(data)

    def output(self, data: Any = None) -> None:
        self.storex.output(data)

    def get_name(self) -> str:
        return self.storex.get_name()

    def get_path(self) -> Path:
        return self.storex.get_path()

    def with_suffix(self, suffix: str) -> Path:
        return self.file_path.with_suffix(suffix)