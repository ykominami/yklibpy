from typing import Any

from yklibpy.common.loggerx import Loggerx
from yklibpy.htmlparser.misc.anchortaginfo import AnchorTagInfo


class HtmlOp:
    @classmethod
    def get_anchor_under_b(cls, child: Any, cond: Any = None) -> list[list[AnchorTagInfo | None]]:
        if cond is None:
            list = child.find_all("b")
        else:
            list = child.find_all("b", cond)
        assoc_array = [cls.get_anchor_all(b_tag) for b_tag in list]

        return assoc_array

    @classmethod
    def get_anchor_all(cls, child: Any) -> list[AnchorTagInfo | None]:
        return [
            cls.get_anchor_tag_info(anchor_tag) for anchor_tag in child.find_all("a")
        ]

    @classmethod
    def get_anchor_tag_info(cls, anchor_tag: Any) -> AnchorTagInfo | None:
        if anchor_tag is None:
            return None

        Loggerx.debug('----', __name__)
        a_tag_info = AnchorTagInfo(anchor_tag)

        return a_tag_info

    @classmethod
    def get_anchor_under_div(cls, child: Any, cond: Any = None) -> None:
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
        tag = assoc["tag"]
        Loggerx.debug(f"1 HtmlOp.print_tag_info: tag={tag}", __name__)

        mes_array = assoc["mes_array"]
        mes = "\n".join(mes_array)
        Loggerx.debug(f"1 HtmlOp.print_tag_info: mes={mes}", __name__)
