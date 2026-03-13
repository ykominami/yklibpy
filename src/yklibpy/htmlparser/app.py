from pathlib import Path
from typing import Any, List

from yklibpy.common.env import Env
from yklibpy.common.loggerx import Loggerx
from yklibpy.htmlparser.scraper import Scraper


class App:
    """HTML ファイル群からリンク情報を集約する実行クラス。"""

    def __init__(self) -> None:
        """リンク集計用の内部状態を初期化する。"""
        self.links_list: list[Any] = []
        self.links_assoc: dict[str, dict[str, Any]] = {}
        self.info: dict[str, Any] = {}
        self.append_count = 0
        self.no_append_count = 0

    def create_scraper(self, mode: str, sequence: int) -> Scraper | None:
        """モードに対応するスクレイパーを生成する。未対応時は `None` を返す。"""
        Loggerx.debug(f"1 App.create_scraper: mode={mode} is not supported", __name__)
        return None

    def loop(self, files: List[Path], mode: str, sequence: int) -> dict[str, dict[str, Any]]:
        """対象ファイルを順に処理し、抽出したリンク情報を結合する。"""
        Loggerx.debug(f"1 App.loop: files={files}", __name__)
        assoc: dict[str, dict[str, Any]] = {}
        for file in files:
            scraper: Scraper | None = self.create_scraper(mode, sequence)
            if scraper is None:
                continue
            extracted_links_assoc = scraper.get_links_assoc_from_html(file)
            if extracted_links_assoc:
                len_extracted_links_assoc = len(extracted_links_assoc)
                if len_extracted_links_assoc > 0:
                    len_assoc = len(assoc)
                    Loggerx.debug(f"0 App.loop: len_assoc={len_assoc}", __name__)
                    assoc.update(extracted_links_assoc)
                    Loggerx.debug(f"1 App.loop: len_assoc={len(assoc)}", __name__)
                else:
                    Loggerx.debug(f"3 App.loop: len_extracted_links_assoc={len_extracted_links_assoc}", __name__)
                    pass
            else:
                Loggerx.debug(f"4 App.loop: extracted_links_assoc={extracted_links_assoc}", __name__)

        return assoc

    def run(self, env: Env) -> None:
        """環境設定から対象ファイルを取得し、リンク情報を収集する。"""
        path_array = env.get_files()
        sequence = env.sequence
        message = f"path_array={path_array} sequence={sequence}"
        # raise Exception(message)
        Loggerx.debug(f"1 App.run: message={message}", __name__)

        mode = env.mode()

        assoc = self.loop(path_array, mode, sequence)
        self.links_assoc.update(assoc)
