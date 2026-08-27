import os
import sys
from pathlib import Path
from typing import Any

from yklibpy.common.loggerx import Loggerx
from yklibpy.common.opresult import OpResult
from yklibpy.common.util import Util
from yklibpy.config.appconfig import AppConfig
from yklibpy.db.storex import Storex


class AppStore:
    """設定ファイルと DB ファイルの保存先解決と入出力を統括する。"""

    def __init__(self, prog_name: str, file_assoc: dict[str, dict[str, dict[str, Any]]], user: str | None, directory_assoc: dict[str, dict[str, dict[str, Any]]] | None = None) -> None:
        """プログラム名と関連付け定義から保存先管理を初期化する。"""
        self.user: str | None = Util.normalize_string(user)
        if Util.is_empty(self.user):
            self.user = None
        self.home_path = Path.home()
        self.prog_name = prog_name
        self.file_assoc = file_assoc
        self.directory_assoc = directory_assoc if directory_assoc is not None else {}
        self.set_ext_name()

    def set_ext_name(self) -> None:
        """`file_assoc` 内の各項目へ拡張子情報を補完する。"""
        try:
            Loggerx.debug(f'1 AppStore.set_ext_name: self.file_assoc={self.file_assoc}', __name__)
            Loggerx.debug(f'2 AppStore.set_ext_name: self.directory_assoc={self.directory_assoc}', __name__)
            for kind in self.file_assoc:
                for base_name in self.file_assoc[kind]:
                    Loggerx.debug(f'3 AppStore.set_ext_name: kind={kind}', __name__)
                    Loggerx.debug(f'4 AppStore.set_ext_name: base_name={base_name}', __name__)
                    Loggerx.debug(f'5 AppStore.set_ext_name: self.file_assoc[kind][base_name]={self.file_assoc[kind][base_name]}', __name__)
                    file_type = self.file_assoc[kind][base_name][AppConfig.FILE_TYPE]
                    self.file_assoc[kind][base_name][AppConfig.EXT_NAME] = Storex.get_ext_name(file_type)
        except KeyError:
            return None

    def prepare_config_file_and_db_file(self) -> None:
        """設定ファイルと DB ファイルの保存先オブジェクトをまとめて準備する。"""
        try:
            self.prepare_config_file()
            self.prepare_db_file()
        except KeyError:
            return None

    def prepare_config_file(self) -> None:
        """設定ファイル群の保存先オブジェクトを準備する。"""
        try:
            kind = AppConfig.KIND_CONFIG
            self.prepare_file_level1(kind)
        except KeyError:
            return None

    def prepare_db_file(self) -> None:
        """DB ファイル群の保存先オブジェクトを準備する。"""
        try:
            kind = AppConfig.KIND_DB
            self.prepare_file_level1(kind)
        except KeyError:
            return None

    def prepare_file_level1(self, kind: str) -> None:
        """指定種別の全ベース名について保存先準備を行う。"""
        try:
            for base_name in self.file_assoc[kind]:
                self.prepare_file_level2(kind, base_name)
        except KeyError:
            return None

    def prepare_file_level2(self, kind: str, base_name: str) -> None:
        """単一のベース名に対する `Storex` を生成して関連付ける。"""
        try:
            # kind = AppConfig.KIND_CONFIG
            file_item_assoc = self.file_assoc[kind][base_name]
            file = self.get_file(self.user, kind, base_name, file_item_assoc)
            if file is None:
                return None
            if self.user is not None:
                self.file_assoc[kind][base_name][AppConfig.PATH][self.user] = file
            else:
                self.file_assoc[kind][base_name][AppConfig.PATH] = file
        except KeyError:
            return None

    def prepare_all_files(self, kind: str) -> None:
        """指定種別に属するすべてのファイル保存先を再構築する。"""
        try:
            # kind = AppConfig.KIND_CONFIG
            for base_name in self.file_assoc[kind]:
                self.prepare_file_level2(kind, base_name)
        except KeyError:
            return None

    def prepare_config_directory_and_db_directory(self) -> None:
        """設定用・DB 用ディレクトリをまとめて準備する。"""
        try:
            self.prepare_config_directory()
            self.prepare_db_directory()
        except KeyError:
            return None

    def prepare_config_directory(self) -> None:
        """設定用ディレクトリ群を準備する。"""
        try:
            self.prepare_directory(AppConfig.KIND_CONFIG)
        except KeyError:
            return None

    def prepare_db_directory(self) -> None:
        """DB 用ディレクトリ群を準備する。"""
        try:
            self.prepare_directory(AppConfig.KIND_DB)
        except KeyError:
            return None

    def prepare_directory(self, kind: str) -> None:
        """指定種別のサブディレクトリを順に作成する。"""
        try:
            for base_name in self.directory_assoc[kind].keys():
                self.prepare_sub_directory(kind, base_name)
        except KeyError:
            return None

    def prepare_all_directory(self) -> None:
        """登録済みの全ディレクトリ種別について準備を行う。"""
        try:
            for kind in self.directory_assoc.keys():
                self.prepare_directory(kind)
        except KeyError:
            return None

    def prepare_sub_directory(self, kind: str, base_name: str) -> None:
        """単一のサブディレクトリを準備する。"""
        try:
            self.mkdir_db(base_name)
        except KeyError:
            return None

    def get_directory_assoc_from_config(self, base_name: str) -> OpResult[Any]:
        """設定用ディレクトリ定義から対象項目を返す。"""
        try:
            if self.user is not None:
                value = self.directory_assoc[AppConfig.KIND_CONFIG][base_name][self.user]
            else:
                value = self.directory_assoc[AppConfig.KIND_CONFIG][base_name]
            return OpResult.success(value)
        except KeyError as exc:
            if self.user is not None:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name} self.user={self.user}"
            else:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name}"
            return OpResult.from_exception(exc, optional_string)

    def get_directory_assoc_from_db(self, base_name: str) -> OpResult[Any]:
        """DB 用ディレクトリ定義から対象項目を返す。"""
        try:
            Loggerx.debug(f'1 AppStore.get_directory_assoc_from_db: self.directory_assoc={self.directory_assoc}', __name__)
            if self.user is not None:
                value = self.directory_assoc[AppConfig.KIND_DB][base_name][self.user]
            else:
                value = self.directory_assoc[AppConfig.KIND_DB][base_name]
            return OpResult.success(value)
        except KeyError as exc:
            if self.user is not None:
                optional_string = f"AppConfig.KIND_DB={AppConfig.KIND_DB} base_name={base_name} self.user={self.user}"
            else:
                optional_string = f"AppConfig.KIND_DB={AppConfig.KIND_DB} base_name={base_name}"
            return OpResult.from_exception(exc, optional_string)

    def load_file_db_all(self) -> None:
        """DB 種別の全ファイルを読み込み、値を関連付けへ反映する。"""
        try:
            kind = AppConfig.KIND_DB
            for base_name in self.file_assoc[kind]:
                if self.user is not None:
                    self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
                else:
                    self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()
        except KeyError:
            return None

    def load_file_db(self, base_name: str) -> None:
        """指定した DB ファイルを読み込み、値を関連付けへ反映する。"""
        try:
            kind = AppConfig.KIND_DB
            if self.user is not None:
                self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
            else:
                self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()
        except KeyError:
            return None

    def load_file_config_all(self) -> None:
        """設定種別の全ファイルを読み込み、値を関連付けへ反映する。"""
        try:
            kind = AppConfig.KIND_CONFIG
            for base_name in self.file_assoc[kind]:
                if self.user is not None:
                    self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
                else:
                    self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()
        except KeyError:
            return None

    def load_file_config(self, base_name: str) -> None:
        """指定した設定ファイルを読み込み、値を関連付けへ反映する。"""
        try:
            kind = AppConfig.KIND_CONFIG
            if self.user is not None:
                self.file_assoc[kind][base_name][AppConfig.VALUE][self.user] = self.file_assoc[kind][base_name][AppConfig.PATH][self.user].load()
            else:
                self.file_assoc[kind][base_name][AppConfig.VALUE] = self.file_assoc[kind][base_name][AppConfig.PATH].load()
        except KeyError:
            return None

    def load_file_all(self) -> None:
        """登録済みの全ファイルを読み込み、値を関連付けへ反映する。"""
        try:
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
        except KeyError:
            return None

    def get_file_assoc_from_config(self, base_name: str) -> OpResult[Any]:
        """設定ファイルから読み込んだ値を返す。"""
        try:
            if self.user is not None:
                value = self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][self.user]
            else:
                value = self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE]
            return OpResult.success(value)
        except KeyError as exc:
            if self.user is not None:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE} self.user={self.user}"
            else:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE}"

            return OpResult.from_exception(exc, optional_string)

    def get_file_assoc_from_db(self, base_name: str) -> OpResult[Any]:
        """DB ファイルから読み込んだ値を返す。"""
        try:
            if self.user is not None:
                value = self.file_assoc[AppConfig.KIND_DB][base_name][AppConfig.VALUE][self.user]
            else:
                value = self.file_assoc[AppConfig.KIND_DB][base_name][AppConfig.VALUE]
            return OpResult.success(value)
        except KeyError as exc:
            if self.user is not None:
                optional_string = f"AppConfig.KIND_DB={AppConfig.KIND_DB} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE} self.user={self.user}"
            else:
                optional_string = f"AppConfig.KIND_DB={AppConfig.KIND_DB} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE}"

            return OpResult.from_exception(exc, optional_string)

    def get_file(self, user: str | None, kind: str, base_name: str, assoc: dict[str, Any]) -> Storex | None:
        """種別に応じて設定用または DB 用の `Storex` を返す。"""
        try:
            if kind == AppConfig.KIND_CONFIG:
                return self.get_config_file(user, base_name, assoc)
            else:
                return self.get_db_file(user, base_name, assoc)
        except KeyError:
            return None

    def get_config_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex | None:
        """現在の OS に応じて設定ファイル用 `Storex` を生成する。"""
        try:
            if sys.platform == "win32":
                # Windows: APPDATA / LOCALAPPDATA
                file_name_array = self.get_config_file_for_win(user, key, assoc[AppConfig.EXT_NAME])
            else:
                # Linux/macOS: XDG規約
                file_name_array = self.get_config_file_for_unix(user, key, assoc[AppConfig.EXT_NAME])

            file = Storex(assoc[AppConfig.FILE_TYPE], file_name_array)
            return file
        except KeyError:
            return None

    def get_db_file(self, user: str | None, key: str, assoc: dict[str, Any]) -> Storex | None:
        """現在の OS に応じて DB ファイル用 `Storex` を生成する。"""
        try:
            file_name_array = []
            if sys.platform == "win32":
                # Windows: APPDATA / LOCALAPPDATA
                file_name_array = self.get_db_file_for_win(user, key, assoc[AppConfig.EXT_NAME])
            else:
                # Linux/macOS: XDG規約
                file_name_array = self.get_db_file_for_unix(user, key, assoc[AppConfig.EXT_NAME])

            file = Storex(assoc[AppConfig.FILE_TYPE], file_name_array)
            return file
        except KeyError:
            return None

    def get_config_file_for_win(self, user: str | None, base_name: str, ext_name: str) -> list[str]:
        """Windows 向けの設定ファイルパス要素列を返す。"""
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
        """Windows 向けの DB ファイルパス要素列を返す。"""
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
        """Unix 系向けの設定ファイルパス要素列を返す。"""
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
        """Unix 系向けの DB ファイルパス要素列を返す。"""
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

    def get_from_config(self, base_name: str, key: str) -> OpResult[Any]:
        """設定値辞書から指定キーの値を取り出す。"""
        try:
            if self.user is not None:
                value = self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][self.user][key]
            else:
                value = self.file_assoc[AppConfig.KIND_CONFIG][base_name][AppConfig.VALUE][key]
            return OpResult.success(value)
        except KeyError as exc:
            if self.user is not None:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE} self.user={self.user} key={key}"
            else:
                optional_string = f"AppConfig.KIND_CONFIG={AppConfig.KIND_CONFIG} base_name={base_name} AppConfig.VALUE={AppConfig.VALUE} key={key} | self.file_assoc[AppConfig.KIND_CONFIG]={self.file_assoc[AppConfig.KIND_CONFIG]} | {self.file_assoc[AppConfig.KIND_CONFIG][base_name]} | self.file_assoc[AppConfig.KIND_CONFIG][base_name]['path'].get_path()={self.file_assoc[AppConfig.KIND_CONFIG][base_name]['path'].get_path()}"
            return OpResult.from_exception(exc, optional_string)

    def output_config(self, key: str, data: dict[str, Any]) -> None:
        """設定ファイルへ辞書データを書き出す。"""
        try:
            Loggerx.debug(f'1 AppStore.output_config: self.user={self.user} key={key} data={data}', __name__)
            if self.user is None:
                Loggerx.debug(f'5 AppStore.output_config: self.user={self.user} ', __name__)
                self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.VALUE] = data
                self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.PATH].output(data)
            else:
                Loggerx.debug(f'2 AppStore.output_config: self.user={self.user}', __name__)
                self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.VALUE] = data
                self.file_assoc[AppConfig.KIND_CONFIG][key][AppConfig.PATH][self.user].output(data)
        except KeyError:
            return None

    def output_db(self, key: str, data: dict[str, Any]) -> None:
        """DB ファイルへ辞書データを書き出す。"""
        try:
            Loggerx.debug("6 AppStore.output_db", __name__)
            if self.user is None:
                Loggerx.debug(f'7 AppStore.output_db: self.file_assoc["db"][key][AppConfig.PATH]={self.file_assoc["db"][key][AppConfig.PATH]}', __name__)
                self.file_assoc[AppConfig.KIND_DB][key][AppConfig.PATH].output(data)
            else:
                self.file_assoc[AppConfig.KIND_DB][key][AppConfig.PATH][self.user].output(data)
        except KeyError:
            return None

    def mkdir_db(self, key: str) -> None:
        """DB 用サブディレクトリを作成し、関連付けへ保存する。"""
        try:
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
        except KeyError:
            return None

    def show(self, kind: str, base_name: str) -> None:
        """読み込み済みデータの内容をデバッグログへ出力する。"""
        try:
            if self.user is None:
                Loggerx.debug(f"7 AppStore.show: user={self.user}", __name__)
                dict_x = self.file_assoc[kind][base_name][AppConfig.VALUE]
            else:
                dict_x = self.file_assoc[kind][base_name][AppConfig.VALUE][self.user]

            for key in dict_x.keys():
                Loggerx.debug(f'8 AppStore.show: key={key}', __name__)
                Loggerx.debug(f'9 AppStore.show: dict_x[key]={dict_x[key]}', __name__)
        except KeyError:
            return None

    def show_config(self, base_name: str) -> None:
        """設定データの内容を表示する。"""
        try:
            self.show(AppConfig.KIND_CONFIG, base_name)
        except KeyError:
            return None

    def show_db(self, base_name: str) -> None:
        """DB データの内容を表示する。"""
        try:
            self.show(AppConfig.KIND_DB, base_name)
        except KeyError:
            return None
