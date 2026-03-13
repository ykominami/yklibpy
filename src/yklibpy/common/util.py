import csv
import inspect
import locale
import re
from io import StringIO
from pathlib import Path
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    TypeVar,
)
from urllib.parse import ParseResult, urlparse

import chardet
from bs4 import Tag

from yklibpy.common.loggerx import Loggerx
from yklibpy.common.util_yaml import UtilYaml

TargetType = Literal["file", "dir", "both"]
T = TypeVar("T")

"""
from __future__ import annotations

import importlib
import inspect
import pkgutil

__all__: list[str] = []

def _export_classes_from_submodules() -> None:
    package_name = __name__
    for modinfo in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        mod_name = modinfo.name

        # Skip private/dunder modules and entrypoints
        if mod_name.startswith("_") or mod_name in {"main"}:
            continue

        module = importlib.import_module(f"{package_name}.{mod_name}")

        for attr_name, obj in vars(module).items():
            if inspect.isclass(obj) and getattr(obj, "__module__", None) == module.__name__:
                globals()[attr_name] = obj
                __all__.append(attr_name)

    # stable, de-duplicated order
    globals()["__all__"] = sorted(set(__all__))

_export_classes_from_submodules()
"""


class Util:
    """文字列処理、パス探索、表形式変換などの汎用処理を集約する。"""

    class UniqueList(Generic[T]):
        """重複を除きつつ追加順を保つリスト。"""

        def __init__(self) -> None:
            """内部の集合と順序付き配列を初期化する。"""
            self._set: set[T] = set()
            self._list: list[T] = []

        def append(self, value: T) -> None:
            """未登録の値だけを末尾へ追加する。"""
            if value not in self._set:
                self._set.add(value)
                self._list.append(value)

        def __iter__(self) -> Iterator[T]:
            """保持順のまま反復できるイテレータを返す。"""
            return iter(self._list)

        def __repr__(self) -> str:
            """デバッグ用に内部リストの表現を返す。"""
            return repr(self._list)

    class Result:
        """URL 検証結果を表す単純なデータ保持クラス。"""

        def __init__(
            self, success: bool, url: str, reason: str, parsed: ParseResult | None
        ) -> None:
            """検証成否、対象 URL、理由、解析結果を保持する。"""
            self.success = success
            self.url = url
            self.reason = reason
            self.parsed = parsed

    @classmethod
    def get_location(cls) -> str:
        """このモジュールファイルの位置を文字列で返す。"""
        return f"{__file__}"

    @classmethod
    def get_location_string(cls) -> str:
        """呼び出し元のファイル名、行番号、関数名を返す。"""
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller = frame.f_back
            filename = Path(caller.f_code.co_filename).name
            lineno = caller.f_lineno
            function = caller.f_code.co_name
            return f"{filename}:{lineno} in {function}"
        return "unknown"

    @classmethod
    def find_paths(
        cls,
        base_dir: Path,
        pattern: str,
        target_type: TargetType = "both",
    ) -> list[Path]:
        """再帰探索で条件に一致するパス一覧を返す。"""
        if not base_dir.is_dir():
            raise ValueError(f"{base_dir} はディレクトリではありません")

        results: list[Path] = []

        Loggerx.debug(f"1 Util.find_paths: base_dir={base_dir}", __name__)
        Loggerx.debug(f"2 pattern={pattern}", __name__)
        for path in base_dir.rglob(pattern):
            Loggerx.debug(f'3 Util.find_paths: path={path}', __name__)
            if target_type == "file" and path.is_file():
                results.append(path)
            elif target_type == "dir" and path.is_dir():
                results.append(path)
            elif target_type == "both":
                results.append(path)

        Loggerx.debug(f"4 Util.find_paths: results={results}", __name__)
        return results

    @classmethod
    def xyz(cls) -> None:
        """簡易動作確認用に固定文字列を出力する。"""
        print("xyz")

    @classmethod
    def list_files(cls, name: str, parts: Sequence[str], suffix: str) -> list[str]:
        """名前、区分、拡張子からファイル名候補を組み立てる。"""
        return [f"{name}-{part}{suffix}" for part in parts]

    @classmethod
    def is_valid_urls(cls, urls: List[str]) -> List["Util.Result"]:
        """URL 一覧を検証し、各要素の結果を配列で返す。"""
        result_array: list[Util.Result] = []
        for url in urls:
            if url == "" or url is None:
                result = cls.Result(False, url, "URL is empty", None)
                result_array.append(result)
                continue

            parsed = urlparse(url)
            if not parsed.scheme:
                result = cls.Result(False, url, "URL scheme is invalid", parsed)
                result_array.append(result)
                continue

            if not parsed.netloc and not parsed.path and not parsed.fragment:
                result = cls.Result(
                    False,
                    url,
                    "URL is not a valid URI: missing authority, path, or fragment",
                    parsed,
                )
                result_array.append(result)
                continue

            result = cls.Result(True, url, "URL is valid", parsed)
            result_array.append(result)

        return result_array

    @classmethod
    def extract_cid(cls, text: str) -> str:
        """文字列から `cid` パラメータ値を抽出する。"""
        m = re.search(r"cid=([^/?&]+)", text)
        return m.group(1) if m else ""

    @classmethod
    def extract_product_id(cls, text: str) -> str:
        """文字列から `product_id` パラメータ値を抽出する。"""
        m = re.search(r"product_id=([^/?&]+)", text)
        return m.group(1) if m else ""

    @classmethod
    def extract_base(cls, base: str, text: str) -> str | None:
        """指定名のクエリパラメータ値を抽出する。"""
        re_text = f"{base}=([^/?&]+)"
        regexp = re.compile(re_text)
        m = regexp.search(text)
        return m.group(1) if m else None

    @classmethod
    def flatten_gen(cls, lst: list[Any]) -> Iterator[Any]:
        """入れ子リストを再帰的に平坦化するジェネレータを返す。"""
        for item in lst:
            if isinstance(item, list):
                yield from Util.flatten_gen(item)
            else:
                yield item

    @classmethod
    def ensure_file_path(cls, path: Path | None) -> Path | None:
        """ファイルと親ディレクトリの存在を保証して返す。"""
        if path is None:
            return None
        if not path.exists():
            parent_path = path.parent
            if not parent_path.exists():
                Loggerx.debug(f'11 Util.ensure_file_path: parent_path={parent_path}', __name__)
                parent_path.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path

    @classmethod
    def ensure_dir_path(cls, path: Path | None) -> Path | None:
        """ディレクトリの存在を保証して返す。"""
        if path is None:
            return None
        Loggerx.debug(f'12 Util.ensure_dir_path: path={path}', __name__)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def flatten(cls, items: Iterable[Any]) -> list[Any]:
        """入れ子の配列を順序を保ったまま 1 次元化する。"""
        flat_list = []
        for item in items:
            if isinstance(item, list):
                flat_list.extend(cls.flatten(item))
            else:
                flat_list.append(item)

        return flat_list

    @classmethod
    def detect_encoding(cls, input_path: Path) -> Optional[str]:
        """ファイル内容から推定される文字エンコーディングを返す。"""
        if input_path is not None:
            with open(input_path, "rb") as f:
                raw = f.read()
                encoding = chardet.detect(raw)["encoding"]
            return encoding
        return None

    @classmethod
    def get_default_encoding(cls) -> str:
        """実行環境の既定エンコーディングを返す。"""
        enc = locale.getpreferredencoding(False)
        return enc

    @classmethod
    def get_common_parents(cls, element1: Tag, element2: Tag) -> List[Tag]:
        """2 つの BeautifulSoup 要素に共通する親タグ一覧を返す。"""

        def get_all_parents(element: Tag) -> List[Tag]:
            """指定要素の親タグをルート方向へ順に集める。"""
            parents = []
            current = element.parent
            while current is not None and hasattr(current, "name"):
                # NavigableStringやNoneを除外し、Tagのみを対象とする
                if isinstance(current, Tag):
                    parents.append(current)
                current = current.parent
            return parents

        parents1 = get_all_parents(element1)
        parents2 = get_all_parents(element2)

        # 共通する親要素を見つける（順序を保持）
        common_parents = []
        # ルートから近い順に比較するため、逆順にする
        parents1_reversed = list(reversed(parents1))
        parents2_reversed = list(reversed(parents2))

        # 両方のリストをセットに変換して高速化
        parents2_set = set(id(p) for p in parents2_reversed)

        # 共通する親要素を順序を保持して取得
        for parent in parents1_reversed:
            if id(parent) in parents2_set:
                common_parents.append(parent)

        return common_parents

    @classmethod
    def load_tsv(
        cls, input_path: Path, fieldnames: Optional[Sequence[str]] = None
    ) -> list[dict[str, str]]:
        """TSV ファイルを読み込み、行ごとの辞書配列へ変換する。"""
        records: list[dict[str, str]] = []
        with open(input_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            headers = list(fieldnames) if fieldnames is not None else None

            for row in reader:
                if headers is None:
                    headers = row
                    continue
                record = {key: value for key, value in zip(headers, row)}
                records.append(record)

        if headers is None:
            raise ValueError("ヘッダー行が存在しません。fieldnamesを指定してください。")

        return records

    @classmethod
    def output_tsv(
        cls,
        records: Sequence[dict[str, str]],
        output_path: Optional[Path] = None,
        fieldnames: Optional[Sequence[str]] = None,
    ) -> str:
        """辞書配列を TSV 文字列へ変換し、必要ならファイルへ出力する。"""
        if not records and fieldnames is None:
            raise ValueError(
                "fieldnamesを指定するか、recordsに1件以上のデータを含めてください。"
            )

        if fieldnames is None:
            headers: list[str] = []
        else:
            headers = list(fieldnames)

        buffer = StringIO()
        writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
        writer.writerow(headers)
        for record in records:
            Loggerx.debug(f"1 Util.output_tsv: record={record}", __name__)
            Loggerx.debug(f"2 Util.output_tsv: headers={headers}", __name__)
            row = [record.get(header, "") for header in headers]
            writer.writerow(row)

        tsv_str = buffer.getvalue()

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                f.write(tsv_str)

        return tsv_str

    def test_yaml(self, input_file: str, input_file_2: str, output_file: str) -> None:
        """Udemy 用 YAML データを比較し、進捗列を引き継いで保存する。"""
        input_path = Path(input_file)
        input_path_2 = Path(input_file_2)
        output_path = Path(output_file)
        dict = UtilYaml.load_yaml(input_path)
        Loggerx.debug(f"1 Util.test_yaml: dict={dict}", __name__)

        dict_2 = UtilYaml.load_yaml(input_path_2)
        #
        output_tsv_path = input_path_2.with_suffix(".tsv")
        output_tsv_path_2 = output_path.with_suffix(".tsv")
        # keys = dict.keys()
        values = list(dict.values())
        Loggerx.debug(f"3 Util.test_yaml: values={values}", __name__)
        keys = values[0].keys()
        Util.output_tsv(values, output_tsv_path, keys)
        # exit()
        values_2 = list(dict_2.values())
        keys_2 = values_2[0].keys()
        Util.output_tsv(values_2, output_tsv_path_2, keys_2)

        for key_2, value_2 in dict_2.items():
            value_2["Time"] = "0時間"
            if key_2 in dict.keys():
                value = dict[key_2]
                if "Time" in value.keys():
                    value_2["Time"] = value["Time"]
            else:
                value_2["Time"] = "0時間"

        UtilYaml.save_yaml(dict_2, output_path)

    def test_tsv(self, input_file: str, input_file_2: str, output_file: str) -> None:
        """Udemy 用 TSV データを比較し、進捗列を引き継いで保存する。"""
        input_path = Path(input_file)
        # yaml_dict = UtilYaml.load_yaml(input_path)

        # input_path = Path('output_2.tsv')
        input_path_2 = Path(input_file_2)
        output_path = Path(output_file)
        records = Util.load_tsv(input_path)
        dict_2 = Util.load_tsv(input_path_2)
        for record_2 in dict_2:
            record_2["Time"] = "0時間"
            # Note: records is a list, not a dict, so this logic may need adjustment
            # Keeping original logic structure but it may not work as intended
            if isinstance(records, list):
                for record in records:
                    if record.get("Course_ID") == record_2.get("Course_ID"):
                        if "Time" in record.keys():
                            record_2["Time"] = record["Time"]
                        break
            else:
                record_2["Time"] = "0時間"
        Util.output_tsv(dict_2, output_path)

    @classmethod
    def remove_crlf(cls, string: str) -> str:
        """文字列から改行コードを取り除く。"""
        # 改行文字のみ抽出
        #newlines = [c for c in string if c in ("\n", "\r")]
        newlines = string.replace("\n", "").replace("\r", "")
        return "".join(newlines)  # ['\n', '\r', '\n', '\n']

    @classmethod
    def remove_whitespace(cls, string: str) -> str:
        """文字列から空白類を取り除く。"""
        # 改行文字のみ抽出
        # whitespace = re.findall(r'\s+', string)
        whitespace = "".join(string.split())
        return "".join(whitespace)  # ['\n', '\r', '\n', '\n']

    @classmethod
    def remove_non_printable(cls, string: str) -> str:
        """文字列から表示不能文字を取り除く。"""
        non_printable = [c for c in string if c.isprintable()]
        return "".join(non_printable)  # ['\n', '\t', '\x00']

    @classmethod
    def get_valid_string(cls, string: str | None) -> str:
        """`None` や空白だけの入力を空文字へ正規化する。"""
        if string is None:
            return ""
        if len(string) == 0:
            return ""
        return cls.remove_whitespace(string)

    @classmethod
    def is_empty(cls, string: str | None) -> bool:
        """入力が実質的に空文字かどうかを判定する。"""
        valid_string = cls.get_valid_string(string)
        return len(valid_string) == 0

    @classmethod
    def normalize_string(cls, string: str | None) -> str | None:
        """有効な文字列だけを返し、空なら `None` を返す。"""
        valid_string = cls.get_valid_string(string)
        if cls.is_empty(valid_string):
            return None
        else:
            return valid_string

    @classmethod
    def array_to_dict(
        cls, data: list[dict[str, Any]], key: str
    ) -> dict[str, dict[str, Any]]:
        """辞書配列を指定キーで引ける連想配列へ変換する。"""
        result: dict[str, dict[str, Any]] = {}
        for item in data:
            if not isinstance(item, dict):
                raise TypeError(
                    f"配列の要素は辞書である必要があります。現在の型: {type(item).__name__}"
                )
            if key not in item:
                raise KeyError(
                    f"キー '{key}' が要素に存在しません。要素のキー: {list(item.keys())}"
                )
            key_value = item[key]
            if not isinstance(key_value, (str, int, float, bool)) or key_value is None:
                raise ValueError(
                    f"キー '{key}' の値は文字列、数値、真偽値である必要があります。現在の型: {type(key_value).__name__}"
                )
            result[str(key_value)] = item

        return result

    @classmethod
    def swap_dict(cls, dict: dict[str, str]) -> dict[str, str]:
        """キーと値を入れ替えた辞書を返す。"""
        return {v: k for k, v in dict.items()} if dict else {}

if __name__ == "__main__":
    # test_util = Util()
    # test_util.test_yaml(input_file="output_udemy_2.yaml", input_file_2="output_udemy_4.yaml", output_file="output_udemy_5.yaml")
    # test_util.test_tsv(input_file="output_udemy_4.tsv", input_file_2="output_udemy_5.tsv", output_file="output_udemy_6.tsv")
    url_str = "https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=d_573976/?dmmref=Basket&i3_ref=recommend&i3_ord=1"
    ret = Util.extract_cid(url_str)
    Loggerx.debug(f"1 Util.main: ret={ret}", __name__)
