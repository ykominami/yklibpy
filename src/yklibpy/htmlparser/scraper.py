from pathlib import Path
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup

from yklibpy.common.info import Info
from yklibpy.common.loggerx import Loggerx
from yklibpy.common.util import Util


class Scraper:
    """HTML からリンク連想配列を構築するスクレイパー基底クラス。"""

    def __init__(self, sequence: int) -> None:
        """抽出結果と中間情報を保持する内部状態を初期化する。"""
        self.sequence = sequence
        self.links_assoc: dict[str, dict[str, Any]] = {}
        self.info: dict[str, Info] = {}
        self.append_count = 0
        self.no_append_count = 0

    @classmethod
    def _to_assoc(cls, title: str, url: str, sequence: int) -> dict[str, Any]:
        """タイトルと URL から標準的なリンク辞書を組み立てる。"""
        return {"title": title, "url": url, "sequence_array": set([sequence])}

    @classmethod
    def _add_assoc(
        cls,
        links_assoc: dict[str, dict[str, Any]],
        key: str,
        sequence: int,
        value_dict: dict[str, Any],
    ) -> bool:
        """キー単位でリンク辞書を追加し、重複時は出現回数情報のみ更新する。"""
        result = False
        link = links_assoc.get(key, None)
        if link is None:
            links_assoc[key] = value_dict
            result = True
        else:
            link["sequence_array"].add(sequence)
            # raise ValueError(f"link is not None: {link}")
        return result

    def _extract_links_assoc_from_info(self, info: Info) -> Dict[str, Dict[str, Any]]:
        """`Info` を元に抽出処理を実行し、リンク連想配列を返す。"""
        self.scrape(info)
        return self.links_assoc

    def _parse_html_file(self, file_path: Path) -> Optional[BeautifulSoup]:
        """HTML ファイルを読み込み、`BeautifulSoup` へ変換する。"""
        try:
            try:
                encoding = Util.detect_encoding(file_path)
            except Exception as e:
                Loggerx.error(f"An error occurred: {e}", __name__)
                Loggerx.error(f"Encoding detection failed for file: {file_path}", __name__)
                return None
            try:
                with file_path.open("r", encoding=encoding) as f:
                    # Create a BeautifulSoup object using the lxml parser
                    # soup = BeautifulSoup(f, 'lxml')
                    soup = BeautifulSoup(f, "html5lib")
                    return soup
            except Exception as e:
                Loggerx.error(f"An error occurred: {e}", __name__)
                Loggerx.error(f"file_path: {file_path}", __name__)
                return None
        except FileNotFoundError:
            Loggerx.error(f"Error: The file at {file_path} was not found.", __name__)
            return None
        except Exception as e:
            Loggerx.error(f"An error occurred: {e}", __name__)
            Loggerx.error(f"file_path: {file_path}", __name__)
            return None

    def scrape(self, info: Info) -> None:
        """実際の抽出処理を行う拡張ポイント。サブクラスで実装する。"""
        pass

    def get_links_assoc_from_html(self, file_path: Path) -> Dict[str, Dict[str, Any]]:
        """HTML ファイルを解析し、抽出結果の連想配列を返す。"""
        assoc = {}
        if file_path.name not in self.info.keys():
            soup = self._parse_html_file(file_path)
            if soup:
                info = Info(file_path, file_path.name, soup, 0, 0)
                self.info[file_path.name] = info
                assoc = self._extract_links_assoc_from_info(info)
        return assoc
