from typing import Optional

from bs4.element import PageElement

from yklibpy.htmlparser.misc.tagx import Tagx


class AnchorTagx(Tagx):
    """アンカー要素の href と表示文字列を扱う `Tagx` 拡張。"""

    def __init__(self, anchor_tag: Optional[PageElement]) -> None:
        """アンカー要素から href とテキストを抜き出して保持する。"""
        super().__init__(anchor_tag, "anchor")
        self.href: str = ""
        self.text: str = ""
        if self.tag is not None:
            if hasattr(self.tag, "get"):
                self.href = self.tag.get("href", "")
            else:
                self.href = ""
            if hasattr(self.tag, "get_text"):
                self.text = self.tag.get_text(strip=True)
            else:
                self.text = ""
            self.mes_href: str = f"  href: {self.href}"
            self.mes_text: str = f"  text: {self.text}"

    def show(self) -> str:
        """href と表示文字列を改行区切りで返す。"""
        return "\n".join([self.mes_href, self.mes_text])
