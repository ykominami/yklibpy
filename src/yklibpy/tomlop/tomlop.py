
# import tomllib  # 3.11以上の場合
import sys
from pathlib import Path
from typing import Any, cast

import toml

from yklibpy.common.loggerx import Loggerx
from yklibpy.common.util_yaml import UtilYaml
from yklibpy.config.appconfig import AppConfig
from yklibpy.tomlop.fileitem import FileItem


class Tomlop:
    _count: int = 0

    def __init__(self) -> None:
        if Tomlop._count == 0:
            FileItem.setup()
            Tomlop._count += 1
        self.data: Any = {}

    def setup(self, ref_file: str | Path | list[str] | list[Path], config_file: str | Path | list[str] | list[Path] | None) -> None:
        self.ref_file_item = FileItem(ref_file)
        self.config_file_item = FileItem(config_file) if config_file is not None else None

    def compare_dict(self, dict1: dict[str, Any], dict2: dict[str, Any]) -> bool:
        """
        引数1と引数2のキーとキーに対応する値が完全に一致しているかを判定する。
        値が連想配列の場合は再帰的に処理する。

        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）

        Returns:
            True: 引数1と引数2のキーとキーに対応する値が完全に一致している場合
            False: 引数1と引数2のキーとキーに対応する値がどれか一つでも一致しない場合
        """
        # キーの集合が一致しない場合はFalse
        if set(dict1.keys()) != set(dict2.keys()):
            return False

        # 各キーと値のペアを比較
        for key in dict1.keys():
            value1 = dict1[key]
            value2 = dict2[key]

            # 両方とも辞書の場合は再帰的に比較
            if isinstance(value1, dict) and isinstance(value2, dict):
                if not self.compare_dict(value1, value2):
                    return False
            # 値が一致しない場合はFalse
            elif value1 != value2:
                return False

        return True

    def merge_dict(self, dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        引数2の連想配列のキーが引数1に存在しない場合、そのキーと値を引数1に追加する。
        値が連想配列の場合は再帰的に処理する。

        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）

        Returns:
            dict1: マージ後の辞書（引数1を直接変更）
        """
        for key, value in dict2.items():
            if key not in dict1:
                # キーが存在しない場合は追加
                dict1[key] = value
            elif isinstance(dict1[key], dict) and isinstance(value, dict):
                # 両方とも辞書の場合は再帰的に処理
                self.merge_dict(dict1[key], value)
        return dict1

    def diff_dict(self, dict1: dict[str, Any], dict2: dict[str, Any]) -> str:
        """
        比較元と比較先の入れ子の連想配列の差分を文字列として返す。
        値が連想配列の場合は再帰的に処理する。

        Args:
            dict1: 比較元の入れ子の連想配列（辞書）
            dict2: 比較先の入れ子の連想配列（辞書）

        Returns:
            差分がない場合: 空文字列
            差分がある場合: 差分の状態を示す見出し行と、差分の内容を示す行からなる文字列
        """
        result_lines = []

        # すべてのキーを収集
        all_keys = set(dict1.keys()) | set(dict2.keys())

        # 各キーについて差分をチェック
        for key in sorted(all_keys):
            if key not in dict2:
                # 比較元のキーのみが存在する場合
                result_lines.append("# 比較元のキーのみ存在")
                result_lines.append(key)
                value_str = self._format_value(dict1[key])
                result_lines.append(f"  {value_str}")
            elif key not in dict1:
                # 比較先のキーのみが存在する場合
                result_lines.append("# 比較先のキーのみ存在")
                result_lines.append(key)
                value_str = self._format_value(dict2[key])
                result_lines.append(f"  {value_str}")
            else:
                # 両方にキーが存在する場合
                value1 = dict1[key]
                value2 = dict2[key]

                # 両方とも辞書の場合は再帰的に処理
                if isinstance(value1, dict) and isinstance(value2, dict):
                    nested_diff = self.diff_dict(value1, value2)
                    if nested_diff:
                        result_lines.append("# 値が異なる")
                        result_lines.append(key)
                        result_lines.append("## 比較元の値")
                        value_str1 = self._format_value(value1)
                        result_lines.append(f"  {value_str1}")
                        result_lines.append("## 比較先の値")
                        value_str2 = self._format_value(value2)
                        result_lines.append(f"  {value_str2}")
                elif value1 != value2:
                    # 値が異なる場合
                    result_lines.append("# 値が異なる")
                    result_lines.append(key)
                    result_lines.append("## 比較元の値")
                    value_str1 = self._format_value(value1)
                    result_lines.append(f"  {value_str1}")
                    result_lines.append("## 比較先の値")
                    value_str2 = self._format_value(value2)
                    result_lines.append(f"  {value_str2}")

        return "\n".join(result_lines) if result_lines else ""

    def _format_value(self, value: Any) -> str:
        """
        値を文字列としてフォーマットする。
        辞書の場合は見やすい形式で表示する。
        """
        if isinstance(value, dict):
            # 辞書の場合は見やすい形式で表示
            items = []
            for k, v in value.items():
                if isinstance(v, dict):
                    items.append(f"{k}: {{...}}")
                else:
                    items.append(f"{k}: {v}")
            return "{" + ", ".join(items) + "}"
        else:
            return str(value)

    def read_toml_external(self, file_path: str | Path) -> dict[str, Any] | None:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                Loggerx.debug(f"1 Tomlop.read_toml_external: file_path = {file_path}", __name__)
                try:
                    data = toml.load(f)
                    self.data = data
                except Exception as e:
                    Loggerx.debug(f"2 Tomlop.read_toml_external: エラー: {e}", __name__)
                    return None

                Loggerx.debug(f"3 Tomlop.read_toml_external: data={data}", __name__)
                Loggerx.debug(f'4 Tomlop.read_toml_external: data["project"]={data["project"]}', __name__)
                Loggerx.debug(f'5 Tomlop.read_toml_external: data["project"]["authors"]={data["project"]["authors"]}', __name__)

                return data
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return None

    def write_toml_external(self, file_path: str | Path, data: Any) -> bool:
        """
        tomlを用いて、引数で渡された連想配列を、引数で指定されたパスに、TOML形式ファイル出力する。

        Args:
            file_path: TOML形式ファイルへのパス
            data: 連想配列（辞書）

        Returns:
            True: 書き込み成功
            False: 書き込み失敗
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                toml.dump(data, f)
            return True
        except Exception as e:
            print(f"ファイルの書き込みに失敗しました: {file_path}")
            print(f"エラー: {e}")
            return False

    def load_toml(self, ref_file: str | Path | None) -> dict[str, Any] | None:
        Loggerx.debug(f"1 Tomlop.load_toml: ref_file={ref_file}", __name__)
        ref = None
        if ref_file:
            ref = self.read_toml_external(ref_file)

        if ref is not None:
            Loggerx.debug(f"2 Tomlop.load_toml: ref.keys()={ref.keys()}", __name__)
            Loggerx.debug("--------------------------------", __name__)

        return ref

    def exec(self) -> None:
        ref = cast(dict[str, Any], self.ref_file_item.storex.load())
        if self.config_file_item is None:
            raise ValueError("config_file_item is not set")
        config = cast(dict[str, Any], self.config_file_item.storex.load())
        self.data = config

        new_config = self.merge_dict(config, ref)
        result = self.compare_dict(new_config, ref)
        Loggerx.debug(f"1 Tomlop.exec: result={result}", __name__)
        Loggerx.debug(f"2 Tomlop.exec: new_config={new_config}", __name__)
        diff_result = self.diff_dict(new_config, ref)
        Loggerx.debug(f"3 Tomlop.exec: diff_result={diff_result}", __name__)
        Loggerx.debug(f"4 Tomlop.exec: diff_result={diff_result}", __name__)

        new_yaml_file = FileItem(["new_pyproject.toml"], new_config)
        diff_yaml_file = FileItem(["diff_pyproject.toml"], diff_result)
        new_yaml_file.output()
        diff_yaml_file.output()

    def main(self) -> None:
        ref_file = None
        ref_file = sys.argv[1] if len(sys.argv) > 1 else None
        config_file = sys.argv[2] if len(sys.argv) > 2 else "pyproject.toml"
        if ref_file is not None:
            self.setup(ref_file, config_file)
            # self.exec()
            ext_name = self.ref_file_item.storex.get_ext_name(AppConfig.FILE_TYPE_YAML)
            # name = self.ref_file_item.storex.get_name()
            new_file_path = self.ref_file_item.with_suffix(ext_name)
            FileItem(new_file_path, self.data).output()

    def toml2yaml(self) -> None:
        src_file = sys.argv[1] if len(sys.argv) > 1 else None
        if src_file is not None:
            self.setup(src_file, None)
            self.read_toml_external(self.ref_file_item.file_path)
            output_path = Path("a.yaml")
            UtilYaml.save_yaml(self.data, output_path)

    def yaml2toml(self) -> None:
        input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
        if input_path is not None:
            data: dict[str, Any] = UtilYaml.load_yaml(input_path)
            Loggerx.debug(f"1 Tomlop.yaml2toml: data={data}", __name__)
            new_file_path = input_path.with_suffix(".toml")
            Loggerx.debug(f"2 Tomlop.yaml2toml: new_file_path={new_file_path}", __name__)


def zmain() -> None:
    tomlop = Tomlop()
    tomlop.main()


def toml2yaml() -> None:
    tomlop = Tomlop()
    tomlop.toml2yaml()


def yaml2toml() -> None:
    tomlop = Tomlop()
    tomlop.yaml2toml()


if __name__ == "__main__":
    tomlop = Tomlop()
    tomlop.main()
