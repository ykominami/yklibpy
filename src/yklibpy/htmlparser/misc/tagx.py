from typing import Optional

from bs4.element import PageElement


class Tagx:
    """BeautifulSoup 要素から表示用情報を抜き出して保持する。"""

    def __init__(self, tag: Optional[PageElement], namex: str) -> None:
        """タグ本体とログ出力向けの文字列表現を初期化する。"""
        self.option: str = ""
        self.tag = tag
        self.strx = str(tag)
        self.type = type(tag)
        self.mes_type = f"  type({namex}): {str(type(namex))}"
        if tag is not None:
            if hasattr(tag, "get_text"):
                self.text = tag.get_text(strip=True)
                self.mes_text = f"  {namex}_text: {self.text}"
            else:
                self.mes_text = f"  {namex}_text: [Nothing]"

            if hasattr(tag, "name"):
                self.mes_name = f"  {namex}.name: {tag.name}"
            else:
                self.mes_name = f"  {namex}.name: [Nothing]"

    def set_option(self, option: str) -> None:
        """外部で整形した補助文字列を保持する。"""
        self.option = option

    def get_option(self) -> str:
        """保持している補助文字列を返す。"""
        return self.option
