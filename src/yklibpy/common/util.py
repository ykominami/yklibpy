import csv
import inspect
import locale
import re
from io import StringIO
from pathlib import Path
from typing import List, Literal, Optional, Sequence
from urllib.parse import ParseResult, urlparse

import chardet
from bs4 import Tag

from .util_yaml import UtilYaml

TargetType = Literal["file", "dir", "both"]

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
    class UniqueList:
        def __init__(self):
            self._set = set()
            self._list = []

        def append(self, value):
            if value not in self._set:
                self._set.add(value)
                self._list.append(value)

        def __iter__(self):
            return iter(self._list)

        def __repr__(self):
            return repr(self._list)

    class Result:
        def __init__(
            self, success: bool, url: str, reason: str, parsed: ParseResult | None
        ):
            self.success = success
            self.url = url
            self.reason = reason
            self.parsed = parsed

    @classmethod
    def get_location(cls) -> str:
        return f"{__file__}"

    @classmethod
    def get_location_string(cls) -> str:
        """現在の位置を文字列で返す"""
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller = frame.f_back
            filename = Path(caller.f_code.co_filename).name
            lineno = caller.f_lineno
            function = caller.f_code.co_name
            return f"{filename}:{lineno} in {function}"
        return "unknown"

    @classmethod
    def xyz(cls):
        print("xyz")

    @classmethod
    def find_paths(
        cls,
        base_dir: Path,
        pattern: str,
        target_type: TargetType = "both",
    ) -> list[Path]:
        """
        指定ディレクトリ配下を再帰的に探索し、パターンに一致するパスを取得する

        :param base_dir: 探索開始ディレクトリ (Path)
        :param pattern: globパターン (例: "*.py", "data_*")
        :param target_type: "file" | "dir" | "both"
        :return: Path のリスト
        """
        if not base_dir.is_dir():
            raise ValueError(f"{base_dir} はディレクトリではありません")

        results: list[Path] = []

        print(f"base_dir={base_dir}")
        # print(f'pattern={pattern}')
        for path in base_dir.rglob(pattern):
            # print(f'path={path}')
            if target_type == "file" and path.is_file():
                results.append(path)
            elif target_type == "dir" and path.is_dir():
                results.append(path)
            elif target_type == "both":
                results.append(path)

        print(f"results={results}")
        return results

    @classmethod
    def list_files(cls, name, parts, suffix):
        list = [f"{name}-{part}{suffix}" for part in parts]
        return list

    @classmethod
    def is_valid_urls(cls, urls: List[str]) -> List["Util.Result"]:
        result_array = []
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
        m = re.search(r"cid=([^/?&]+)", text)
        return m.group(1) if m else ""

    @classmethod
    def extract_product_id(cls, text: str) -> str:
        m = re.search(r"product_id=([^/?&]+)", text)
        return m.group(1) if m else ""

    @classmethod
    def extract_base(cls, base: str, text: str) -> str | None:
        re_text = f"{base}=([^/?&]+)"
        regexp = re.compile(re_text)
        m = regexp.search(text)
        return m.group(1) if m else None

    @classmethod
    def flatten_gen(cls, lst):
        for item in lst:
            if isinstance(item, list):
                yield from Util.flatten_gen(item)
            else:
                yield item

    @classmethod
    def ensure_file_path(cls, path: Path | None) -> Path | None:
        if path is None:
            return None
        if not path.exists():
            parent_path = path.parent
            if not parent_path.exists():
                parent_path.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path

    @classmethod
    def ensure_dir_path(cls, path: Path | None) -> Path | None:
        if path is None:
            return None
        path.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def flatten(cls, items):
        """Flatten arbitrarily nested iterables into a single list.

        Args:
            items (Iterable): Possibly nested lists/tuples of values.

        Returns:
            list: Flattened sequence preserving order.
        """
        flat_list = []
        for item in items:
            if isinstance(item, list):
                flat_list.extend(cls.flatten(item))
            else:
                flat_list.append(item)

        return flat_list

    @classmethod
    def detect_encoding(cls, input_path: Path) -> Optional[str]:
        if input_path is not None:
            with open(input_path, "rb") as f:
                raw = f.read()
                encoding = chardet.detect(raw)["encoding"]
            return encoding
        return None

    @classmethod
    def get_default_encoding(cls) -> str:
        enc = locale.getpreferredencoding(False)
        return enc

    @classmethod
    def get_common_parents(cls, element1: Tag, element2: Tag) -> List[Tag]:
        """2つのBeautifulSoup要素の共通する親要素をすべて取得する。

        Args:
            element1 (Tag): 最初の要素
            element2 (Tag): 2番目の要素

        Returns:
            List[Tag]: 共通する親要素のリスト（ルートから近い順、つまり最も近い共通親が最後）

        Examples:
            >>> from bs4 import BeautifulSoup
            >>> soup = BeautifulSoup('<div><p><span>text1</span></p><p><span>text2</span></p></div>', 'html.parser')
            >>> span1 = soup.find_all('span')[0]
            >>> span2 = soup.find_all('span')[1]
            >>> common_parents = Util.get_common_parents(span1, span2)
            >>> # [<div>...</div>, <html>...</html>, <body>...</body>] などが返される
        """

        def get_all_parents(element: Tag) -> List[Tag]:
            """要素のすべての親要素をルートまで取得する"""
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
    ) -> list[dict]:
        """Read a TSV file and convert rows into dictionaries.

        Args:
            input_path (Path): TSV file path.
            fieldnames (Sequence[str] | None): Explicit headers. When ``None`` the
                first row becomes the header.

        Returns:
            list[dict]: Each row keyed by the header columns.

        Raises:
            ValueError: If no headers can be determined.
        """
        records = []
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
        records: Sequence[dict],
        output_path: Optional[Path] = None,
        fieldnames: Optional[Sequence[str]] = None,
    ) -> str:
        """Write record dictionaries to TSV format.

        Args:
            records (Sequence[dict]): Rows to emit.
            output_path (Path | None): Optional destination file.
            fieldnames (Sequence[str] | None): Header order override; defaults to
                keys of the first record.

        Returns:
            str: TSV string containing the headers and rows.

        Raises:
            ValueError: If neither records nor ``fieldnames`` are provided.
        """
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
            # print(record)
            # print(headers)
            row = [record.get(header, "") for header in headers]
            writer.writerow(row)

        tsv_str = buffer.getvalue()

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                f.write(tsv_str)

        return tsv_str

    def test_yaml(self, input_file: str, input_file_2: str, output_file: str):
        """Developer helper for merging Udemy YAML progress data.

        Returns:
          None
        """
        input_path = Path(input_file)
        input_path_2 = Path(input_file_2)
        output_path = Path(output_file)
        dict = UtilYaml.load_yaml(input_path)
        # print(dict)

        dict_2 = UtilYaml.load_yaml(input_path_2)
        #
        output_tsv_path = input_path_2.with_suffix(".tsv")
        output_tsv_path_2 = output_path.with_suffix(".tsv")
        # keys = dict.keys()
        values = list(dict.values())
        # print(values)
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

    def test_tsv(self, input_file: str, input_file_2: str, output_file: str):
        """Developer helper for merging Udemy TSV progress data.

        Returns:
          None
        """
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


if __name__ == "__main__":
    # test_util = Util()
    # test_util.test_yaml(input_file="output_udemy_2.yaml", input_file_2="output_udemy_4.yaml", output_file="output_udemy_5.yaml")
    # test_util.test_tsv(input_file="output_udemy_4.tsv", input_file_2="output_udemy_5.tsv", output_file="output_udemy_6.tsv")
    url_str = "https://www.dmm.co.jp/dc/doujin/-/detail/=/cid=d_573976/?dmmref=Basket&i3_ref=recommend&i3_ord=1"
    ret = Util.extract_cid(url_str)
    print(ret)
