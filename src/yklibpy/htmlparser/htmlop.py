from typing import Any

from yklibpy.common.loggerx import Loggerx
from yklibpy.htmlparser.misc.anchortaginfo import AnchorTagInfo


class HtmlOp:
    """BeautifulSoup 要素からアンカー情報を取り出す補助クラス。"""

    @classmethod
    def get_anchor_under_b(cls, child: Any, cond: Any = None) -> list[list[AnchorTagInfo | None]]:
        """`b` 要素配下のアンカー情報を配列で返す。"""
        if cond is None:
            list = child.find_all("b")
        else:
            list = child.find_all("b", cond)
        assoc_array = [cls.get_anchor_all(b_tag) for b_tag in list]

        return assoc_array

    @classmethod
    def get_anchor_all(cls, child: Any) -> list[AnchorTagInfo | None]:
        """要素配下のすべてのアンカーを `AnchorTagInfo` へ変換する。"""
        return [
            cls.get_anchor_tag_info(anchor_tag) for anchor_tag in child.find_all("a")
        ]

    @classmethod
    def get_anchor_tag_info(cls, anchor_tag: Any) -> AnchorTagInfo | None:
        """単一のアンカー要素から `AnchorTagInfo` を作成する。"""
        if anchor_tag is None:
            return None

        Loggerx.debug('----', __name__)
        a_tag_info = AnchorTagInfo(anchor_tag)

        return a_tag_info

    @classmethod
    def get_anchor_under_div(cls, child: Any, cond: Any = None) -> None:
        """`div` 要素配下のアンカー情報をログへ出力する。"""
        if cond is None:
            list = child.find_all("div", cond)
        else:
            list = child.find_all("div")

        for div_tag in list:
            Loggerx.debug(f"1 HtmlOp.get_anchor_under_div: div_tag={div_tag}", __name__)
            anchor_tag_info_array = HtmlOp.get_anchor_all(div_tag)
            for anchor_tag_info in anchor_tag_info_array:
                cls.print_tag_info(anchor_tag_info)

    @classmethod
    def print_tag_info(cls, assoc: Any) -> None:
        """アンカー情報辞書の内容をデバッグログへ整形出力する。"""
        tag = assoc["tag"]
        Loggerx.debug(f"1 HtmlOp.print_tag_info: tag={tag}", __name__)

        mes_array = assoc["mes_array"]
        mes = "\n".join(mes_array)
        Loggerx.debug(f"1 HtmlOp.print_tag_info: mes={mes}", __name__)
