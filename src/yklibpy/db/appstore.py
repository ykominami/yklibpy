import os
import sys
from pathlib import Path
from typing import Any

from yklibpy.common.util import Util
from yklibpy.db.storex import Storex


class AppStore:
    def __init__(self, prog_name: str, assoc: dict[str, dict[str, dict[str, Any]]], user: str | None) -> None:
        self.user = Util.normalize_string(user)
        self.home_path = Path.home()
        self.prog_name = prog_name
        self.assoc = assoc
        self.set_ext_name()

    def set_ext_name(self):
        for kind in self.assoc:
            for base_name in self.assoc[kind]:
                self.assoc[kind][base_name]["ext_name"] = Storex.get_ext_name(
                    self.assoc[kind][base_name]["file_type"]
                )

    def prepare_config_file_and_db_file(self):
        for kind in self.assoc:
            for base_name in self.assoc[kind]:
                file_item_assoc = self.assoc[kind][base_name]
                file = self.get_file(self.user, kind, base_name, file_item_assoc)

                # print(f'4 Yklibpy AppStore prepare_config_file_and_db_file self.user={self.user} ')
                # print(f'5 self.assoc[kind][base_name]={self.assoc[kind][base_name]}')
                if self.user is not None:
                    self.assoc[kind][base_name]["file"][self.user] = file
                else:
                    self.assoc[kind][base_name]["file"] = file

        return self.assoc

    def load_file(self) -> None:
        for kind in self.assoc:
            for base_name in self.assoc[kind]:
                if self.user is not None:
                    # print(f'1 Yklibpy AppStore load_file self.user={self.user} self.assoc[kind][base_name]={self.assoc[kind][base_name]}')
                    self.assoc[kind][base_name]["value"][self.user] = self.assoc[kind][base_name][
                        "file"
                    ][self.user].load()
                else:
                    # print(f'2 Yklibpy AppStore load_file self.user={self.user} ')
                    self.assoc[kind][base_name]["value"] = self.assoc[kind][base_name][
                        "file"
                    ].load()

    def get_assoc_from_config(self, base_name: str) -> Any:
        if self.user is not None:
            return self.assoc["config"][base_name]["value"][self.user]
        else:
            return self.assoc["config"][base_name]["value"]

    def get_assoc_from_db(self, base_name: str) -> Any:
        if self.user is not None:
            return self.assoc["db"][base_name]["value"][self.user]
        else:
            return self.assoc["db"][base_name]["value"]

    def get_file(self, user: str | None, kind: str, base_name: str, assoc: dict[str, Any]) -> Storex:
        if kind == "config":
            return self.get_config_file(user, base_name, assoc)
        else:
            return self.get_db_file(user, base_name, assoc)

    def get_config_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex:
        if sys.platform == "win32":
            # Windows: APPDATA / LOCALAPPDATA
            file_name_array = self.get_config_file_for_win(user, key, assoc["ext_name"])
        else:
            # Linux/macOS: XDG規約
            file_name_array = self.get_config_file_for_unix(user, key, assoc["ext_name"])

        file = Storex(assoc["file_type"], file_name_array)
        return file

    def get_db_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex:
        file_name_array = []
        if sys.platform == "win32":
            # Windows: APPDATA / LOCALAPPDATA
            file_name_array = self.get_db_file_for_win(user, key, assoc["ext_name"])
        else:
            # Linux/macOS: XDG規約
            file_name_array = self.get_db_file_for_unix(user, key, assoc["ext_name"])

        file = Storex(assoc["file_type"], file_name_array)
        return file

    def get_config_file_for_win(self, user: str | None, base_name: str, ext_name: str):
        config_top_dir = Path(
            os.environ.get("APPDATA", str(self.home_path / "AppData" / "Roaming"))
        )
        file_name = f"{base_name}{ext_name}"
        if user is not None:
            config_file_name_array = [str(config_top_dir),  self.prog_name, user, file_name]
        else:
            config_file_name_array = [str(config_top_dir),  self.prog_name, file_name]

        return config_file_name_array

    def get_db_file_for_win(self, user: str | None,base_name: str, ext_name: str):
        data_top_dir = Path(
            os.environ.get("LOCALAPPDATA", str(self.home_path / "AppData" / "Local"))
        )
        file_name = f"{base_name}{ext_name}"
        if user is not None:
            db_file_name_array = [str(data_top_dir), self.prog_name, user, file_name]
        else:
            db_file_name_array = [str(data_top_dir), self.prog_name, file_name]

        return db_file_name_array

    def get_config_file_for_unix(self, user: str | None,base_name: str, ext_name: str):
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
            # print(f'3 Yklibpy AppStore get_config_file_for_unix user={user} ')
            config_file_name_array = [
                str(self.home_path),
                ".config",
                self.prog_name,
                file_name,
            ]
            
        return config_file_name_array

    def get_db_file_for_unix(self, user: str | None, base_name: str, ext_name: str):
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
            # print(f'4 Yklibpy AppStore get_db_file_for_unix user={user} ')
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
            return self.assoc["config"][base_name]["value"][self.user][key]
        else:
            return self.assoc["config"][base_name]["value"][key]

    def output_config(self, key: str, data: dict[str, Any]) -> None:
        # print( f'Yklibpy AppStore output_config self.user={self.user} key={key} data={data}' )
        if self.user is None:
            # print(f'5 Yklibpy AppStore output_config self.user={self.user} ')
            self.assoc["config"][key]["file"].output(data)
        else:
            # print( f'2 Yklibpy AppStore output_config self.user={self.user}' )
            self.assoc["config"][key]["file"][self.user].output(data)

    def output_db(self, key: str, data: dict[str, Any]) -> None:
        # print(f'6 Yklibpy AppStore output_db')
        if self.user is None:
            #print(f'7 self.assoc["d"b"][key]["file"]={self.assoc["db"][key]["file"]}')
            self.assoc["db"][key]["file"].output(data)
        else:
            self.assoc["db"][key]["file"][self.user].output(data)

    def show(self, kind: str, base_name: str) -> None:
        if self.user is None:
            # print(f'7 Yklibpy AppStore show user={user} ')
            dict_x = self.assoc[kind][base_name]["value"]
        else:
            dict_x = self.assoc[kind][base_name]["value"][self.user]

        for key in dict_x.keys():
            print( f'key={key}' )
            print( dict_x[key])

    def show_config(self, user: str | None, base_name: str) -> None:
        self.show(user, "config", base_name)

    def show_db(self, user: str | None, base_name: str) -> None:
        self.show(user, "db", base_name)
