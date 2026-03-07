import os
import sys
from pathlib import Path
from typing import Any

from yklibpy.common.loggerx import Loggerx
from yklibpy.common.util import Util
from yklibpy.config.appconfig import AppConfig
from yklibpy.db.storex import Storex


class AppStore:
    def __init__(self, prog_name: str, file_assoc: dict[str, dict[str, dict[str, Any]]], user: str | None, directory_assoc: dict[str, dict[str, dict[str, Any]]] | None = None) -> None:
        self.user = Util.normalize_string(user)
        if Util.is_empty(self.user):
            self.user = None
        self.home_path = Path.home()
        self.prog_name = prog_name
        self.file_assoc = file_assoc
        self.directory_assoc = directory_assoc if directory_assoc is not None else {}
        self.set_ext_name()

    def set_ext_name(self) -> None:
        Loggerx.debug(f'1 AppStore.set_ext_name: self.file_assoc={self.file_assoc}', __name__)
        Loggerx.debug(f'2 AppStore.set_ext_name: self.directory_assoc={self.directory_assoc}', __name__)
        for kind in self.file_assoc:
            for base_name in self.file_assoc[kind]:
                Loggerx.debug(f'3 AppStore.set_ext_name: kind={kind}', __name__)
                Loggerx.debug(f'4 AppStore.set_ext_name: base_name={base_name}', __name__)
                Loggerx.debug(f'5 AppStore.set_ext_name: self.file_assoc[kind][base_name]={self.file_assoc[kind][base_name]}', __name__)
                file_type = self.file_assoc[kind][base_name][AppConfig.FILE_TYPE]
                self.file_assoc[kind][base_name][AppConfig.EXT_NAME] = Storex.get_ext_name(file_type)

    def prepare_config_file_and_db_file(self) -> None:
        self.prepare_config_file()
        self.prepare_db_file()

    def prepare_config_file(self) -> None:
        kind = AppConfig.KIND_CONFIG
        self.prepare_file_level1(kind)

    def prepare_db_file(self) -> None:
        kind = AppConfig.KIND_DB
        self.prepare_file_level1(kind)

    def prepare_file_level1(self, kind: str) -> None:
        for base_name in self.file_assoc[kind]:
            self.prepare_file_level2(kind, base_name)

    def prepare_file_level2(self, kind: str, base_name: str) -> None:
        # kind = AppConfig.KIND_CONFIG
        file_item_assoc = self.file_assoc[kind][base_name]
        file = self.get_file(self.user, kind, base_name, file_item_assoc)
        if self.user is not None:
            self.file_assoc[kind][base_name][AppConfig.PATH][self.user] = file
        else:
            self.file_assoc[kind][base_name][AppConfig.PATH] = file

    def prepare_all_files(self, kind: str) -> None:
        # kind = AppConfig.KIND_CONFIG
        for base_name in self.file_assoc[kind]:
            self.prepare_file_level2(kind, base_name)

    def prepare_config_directory_and_db_directory(self) -> None:
        self.prepare_config_directory()
        self.prepare_db_directory()

    def prepare_config_directory(self) -> None:
        self.prepare_directory(AppConfig.KIND_CONFIG)

    def prepare_db_directory(self) -> None:
        self.prepare_directory(AppConfig.KIND_DB)

    def prepare_directory(self, kind: str) -> None:
        for base_name in self.directory_assoc[kind].keys():
            self.prepare_sub_directory(kind, base_name)

    def prepare_all_directory(self) -> None:
        for kind in self.directory_assoc.keys():
            self.prepare_directory(kind)

    def prepare_sub_directory(self, kind: str, base_name: str) -> None:
        self.mkdir_db(base_name)

    def get_directory_assoc_from_config(self, base_name: str) -> Any:
        if self.user is not None:
            return self.directory_assoc[AppConfig.KIND_CONFIG][base_name][self.user]
        else:
            return self.directory_assoc[AppConfig.KIND_CONFIG][base_name]

    def get_directory_assoc_from_db(self, base_name: str) -> Any:
        Loggerx.debug(f'1 AppStore.get_directory_assoc_from_db: self.directory_assoc={self.directory_assoc}', __name__)
        if self.user is not None:
            return self.directory_assoc[AppConfig.KIND_DB][base_name][self.user]
        else:
            return self.directory_assoc[AppConfig.KIND_DB][base_name]

    def load_file_db_all(self) -> None:
        kind = AppConfig.KIND_DB
        for base_name in self.file_assoc[kind]:
            if self.user is not None:
                self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
            else:
                self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()

    def load_file_db(self, base_name: str) -> None:
        kind = AppConfig.KIND_DB
        if self.user is not None:
            self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
        else:
            self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()

    def load_file_config_all(self) -> None:
        kind = AppConfig.KIND_CONFIG
        for base_name in self.file_assoc[kind]:
            if self.user is not None:
                self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
            else:
                self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()

    def load_file_config(self, base_name: str) -> None:
        kind = AppConfig.KIND_CONFIG
        if self.user is not None:
            self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
        else:
            self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()

    def load_file_all(self) -> None:
        for kind in self.file_assoc:
            for base_name in self.file_assoc[kind]:
                if self.user is not None:
                    Loggerx.debug(f'1 AppStore.load_file: self.user={self.user} self.file_assoc[kind][base_name]={self.file_assoc[kind][base_name]}', __name__)
                    self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][
                        AppConfig.PATH
                    ][self.user].load()
                else:
                    Loggerx.debug(f'2 AppStore.load_file: self.user={self.user} ', __name__)
                    self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][
                        AppConfig.PATH
                    ].load()

    def get_file_assoc_from_config(self, base_name: str) -> Any:
        if self.user is not None:
            return self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][self.user]
        else:
            return self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE]

    def get_file_assoc_from_db(self, base_name: str) -> Any:
        if self.user is not None:
            return self.file_assoc[AppConfig.KIND_DB][base_name][AppConfig.VALUE][self.user]
        else:
            return self.file_assoc[AppConfig.KIND_DB][base_name][AppConfig.VALUE]

    def get_file(self, user: str | None, kind: str, base_name: str, assoc: dict[str, Any]) -> Storex:
        if kind == AppConfig.KIND_CONFIG:
            return self.get_config_file(user, base_name, assoc)
        else:
            return self.get_db_file(user, base_name, assoc)

    def get_config_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex:
        if sys.platform == "win32":
            # Windows: APPDATA / LOCALAPPDATA
            file_name_array = self.get_config_file_for_win(user, key, assoc[AppConfig.EXT_NAME])
        else:
            # Linux/macOS: XDG規約
            file_name_array = self.get_config_file_for_unix(user, key, assoc[AppConfig.EXT_NAME])

        file = Storex(assoc[AppConfig.FILE_TYPE], file_name_array)
        return file

    def get_db_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex:
        file_name_array = []
        if sys.platform == "win32":
            # Windows: APPDATA / LOCALAPPDATA
            file_name_array = self.get_db_file_for_win(user, key, assoc[AppConfig.EXT_NAME])
        else:
            # Linux/macOS: XDG規約
            file_name_array = self.get_db_file_for_unix(user, key, assoc[AppConfig.EXT_NAME])

        file = Storex(assoc[AppConfig.FILE_TYPE], file_name_array)
        return file

    def get_config_file_for_win(self, user: str | None, base_name: str, ext_name: str) -> list[str]:
        config_top_dir = Path(
            os.environ.get("APPDATA", str(self.home_path / "AppData" / "Roaming"))
        )
        file_name = f"{base_name}{ext_name}"
        if user is not None:
            config_file_name_array = [str(config_top_dir),  self.prog_name, user, file_name]
        else:
            config_file_name_array = [str(config_top_dir),  self.prog_name, file_name]

        return config_file_name_array

    def get_db_file_for_win(self, user: str | None,base_name: str, ext_name: str) -> list[str]:
        data_top_dir = Path(
            os.environ.get("LOCALAPPDATA", str(self.home_path / "AppData" / "Local"))
        )
        file_name = f"{base_name}{ext_name}"
        if user is not None:
            db_file_name_array = [str(data_top_dir), self.prog_name, user, file_name]
        else:
            db_file_name_array = [str(data_top_dir), self.prog_name, file_name]

        return db_file_name_array

    def get_config_file_for_unix(self, user: str | None,base_name: str, ext_name: str) -> list[str]:
        file_name = f"{base_name}{ext_name}"
        if  user is not None:
            config_file_name_array = [
                str(self.home_path),
                ".config",
                self.prog_name,
                user,
                file_name,
            ]
        else:
            Loggerx.debug(f'3 AppStore.get_config_file_for_unix: user={user} ', __name__)
            config_file_name_array = [
                str(self.home_path),
                ".config",
                self.prog_name,
                file_name,
            ]
            
        return config_file_name_array

    def get_db_file_for_unix(self, user: str | None, base_name: str, ext_name: str) -> list[str]:
        file_name = f"{base_name}{ext_name}"
        if user is not None and user != "":
            db_file_name_array = [
                str(self.home_path),
                ".local",
                "share",
                self.prog_name,
                user,
                file_name,
            ]

        else:
            Loggerx.debug(f'4 AppStore.get_db_file_for_unix: user={user} ', __name__)
            db_file_name_array = [
                str(self.home_path),
                ".local",
                "share",
                self.prog_name,
                file_name,
            ]
        return db_file_name_array

    def get_from_config(self, base_name: str, key: str) -> Any:
        if self.user is not None:
            return self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][self.user][key]
        else:
            return self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][key]

    def output_config(self, key: str, data: dict[str, Any]) -> None:
        Loggerx.debug(f'1 AppStore.output_config: self.user={self.user} key={key} data={data}', __name__)
        if self.user is None:
            Loggerx.debug(f'5 AppStore.output_config: self.user={self.user} ', __name__)
            self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.PATH].output(data)
        else:
            Loggerx.debug(f'2 AppStore.output_config: self.user={self.user}', __name__)
            self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.PATH][self.user].output(data)

    def output_db(self, key: str, data: dict[str, Any]) -> None:
        Loggerx.debug("6 AppStore.output_db", __name__)
        if self.user is None:
            Loggerx.debug(f'7 AppStore.output_db: self.file_assoc["db"][key][AppConfig.PATH]={self.file_assoc["db"][key][AppConfig.PATH]}', __name__)
            self.file_assoc[AppConfig.KIND_DB][key][AppConfig.PATH].output(data)
        else:
            self.file_assoc[AppConfig.KIND_DB][key][AppConfig.PATH][self.user].output(data)

    def mkdir_db(self, key: str) -> None:
        if sys.platform == "win32":
            data_top_dir = os.environ.get("LOCALAPPDATA", str(self.home_path / "AppData" / "Local"))
            data_top_dir_path = Path(data_top_dir)
        else:
            data_top_dir_path = self.home_path / ".local" / "share"

        dir_path = data_top_dir_path / self.prog_name / key

        dir_path.mkdir(parents=True, exist_ok=True)
        Loggerx.debug(f'10 AppStore.mkdir_db: dir_path={dir_path}', __name__)

        self.directory_assoc[AppConfig.KIND_DB][key][AppConfig.PATH] = {}
        if self.user is not None:
            self.directory_assoc[AppConfig.KIND_DB][key][AppConfig.PATH][self.user] = dir_path
        else:
            self.directory_assoc[AppConfig.KIND_DB][key][AppConfig.PATH] = dir_path

    def show(self, kind: str, base_name: str) -> None:
        if self.user is None:
            Loggerx.debug(f"7 AppStore.show: user={self.user}", __name__)
            dict_x = self.file_assoc[kind][base_name][AppConfig.VALUE]
        else:
            dict_x = self.file_assoc[kind][base_name][AppConfig.VALUE][self.user]

        for key in dict_x.keys():
            Loggerx.debug(f'8 AppStore.show: key={key}', __name__)
            Loggerx.debug(f'9 AppStore.show: dict_x[key]={dict_x[key]}', __name__)

    def show_config(self, base_name: str) -> None:
        self.show(AppConfig.KIND_CONFIG, base_name)

    def show_db(self, base_name: str) -> None:
        self.show(AppConfig.KIND_DB, base_name)
