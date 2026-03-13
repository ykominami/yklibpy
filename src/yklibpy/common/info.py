from pathlib import Path

from bs4 import BeautifulSoup


class Info:
    """解析済み HTML と処理件数をひとまとめに保持する。"""

    def __init__(
        self,
        file_path: Path,
        name: str,
        soup: BeautifulSoup,
        append_count: int,
        no_append_count: int,
    ) -> None:
        """入力ファイルと DOM、集計用カウンタを初期化する。"""
        self.file_path = file_path
        self.name = name
        self.soup = soup
        self.append_count = append_count
        self.no_append_count = no_append_count
