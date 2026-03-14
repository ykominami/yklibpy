
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
    """TOML と YAML の比較、変換、差分出力を扱う。

    設定ファイルの補完やフォーマット変換を CLI から実行する用途を想定する。
    """

    _count: int = 0

    def __init__(self) -> None:
        """共有初期化を一度だけ行い、作業用データを空にする。"""
        if Tomlop._count == 0:
            FileItem.setup()
            Tomlop._count += 1
        self.data: Any = {}

    def setup(self, ref_file: str | Path | list[str] | list[Path], config_file: str | Path | list[str] | list[Path] | None) -> None:
        """参照元ファイルと設定ファイルの `FileItem` を準備する。

        Args:
            ref_file: 比較元または変換元になるファイル。
            config_file: 比較先設定ファイル。不要な場合は `None` を許容する。
        """
        self.ref_file_item = FileItem(ref_file)
        self.config_file_item = FileItem(config_file) if config_file is not None else None

    def compare_dict(self, dict1: dict[str, Any], dict2: dict[str, Any]) -> bool:
        """2 つの辞書が再帰的に完全一致するかを判定する。"""
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
        """不足キーだけを `dict2` から `dict1` へ補完する。

        既存キーは維持し、双方が辞書のときだけ再帰的に掘り下げる。
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
        """2 つの辞書の差分を可読な文字列として返す。

        片方にしか存在しないキーと、値が異なるキーを見分けて整形する。
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
        """差分表示用に値を短い文字列へ整形する。"""
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
        """外部 TOML ファイルを読み込み、内容を返す。

        Returns:
            読み込みに成功した辞書。失敗時は `None`。
        """
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
            Loggerx.error(f"ファイルが見つかりません: {file_path}", __name__)
            return None

    def write_toml_external(self, file_path: str | Path, data: Any) -> bool:
        """辞書データを外部 TOML ファイルへ書き出す。

        Returns:
            書き込みに成功したときは `True`、失敗したときは `False`。
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                toml.dump(data, f)
            return True
        except Exception as e:
            Loggerx.error(f"ファイルの書き込みに失敗しました: {file_path}", __name__)
            Loggerx.error(f"エラー: {e}", __name__)
            return False

    def load_toml(self, ref_file: str | Path | None) -> dict[str, Any] | None:
        """参照用 TOML を読み込み、内容を返す。

        `ref_file` が未指定なら何も読まずに `None` を返す。
        """
        Loggerx.debug(f"1 Tomlop.load_toml: ref_file={ref_file}", __name__)
        ref = None
        if ref_file:
            ref = self.read_toml_external(ref_file)

        if ref is not None:
            Loggerx.debug(f"2 Tomlop.load_toml: ref.keys()={ref.keys()}", __name__)
            Loggerx.debug("--------------------------------", __name__)

        return ref

    def exec(self) -> None:
        """参照ファイルとの差分を計算し、補完結果と差分を出力する。

        Raises:
            ValueError: 比較対象の設定ファイルが未設定の場合。
        """
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
        """CLI 引数を解釈して主要処理を起動する。

        参照ファイルが指定された場合だけ、出力先拡張子を決めて結果を書き出す。
        """
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
        """指定した TOML を読み込み、YAML ファイルへ変換する。"""
        src_file = sys.argv[1] if len(sys.argv) > 1 else None
        if src_file is not None:
            self.setup(src_file, None)
            self.read_toml_external(self.ref_file_item.file_path)
            output_path = Path("a.yaml")
            UtilYaml.save_yaml(self.data, output_path)

    def yaml2toml(self) -> None:
        """指定した YAML を読み込み、TOML ファイルへ変換する。

        読み込み後の出力先パスだけを確定し、後続処理に備える。
        """
        input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
        if input_path is not None:
            data: dict[str, Any] = UtilYaml.load_yaml(input_path)
            Loggerx.debug(f"1 Tomlop.yaml2toml: data={data}", __name__)
            new_file_path = input_path.with_suffix(".toml")
            Loggerx.debug(f"2 Tomlop.yaml2toml: new_file_path={new_file_path}", __name__)


def zmain() -> None:
    """`Tomlop.main()` を起動する単純なエントリポイント。"""
    tomlop = Tomlop()
    tomlop.main()


def toml2yaml() -> None:
    """`Tomlop.toml2yaml()` を起動する単純なエントリポイント。"""
    tomlop = Tomlop()
    tomlop.toml2yaml()


def yaml2toml() -> None:
    """`Tomlop.yaml2toml()` を起動する単純なエントリポイント。"""
    tomlop = Tomlop()
    tomlop.yaml2toml()


if __name__ == "__main__":
    tomlop = Tomlop()
    tomlop.main()
