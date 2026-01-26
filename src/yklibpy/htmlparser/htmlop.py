from yklibpy.htmlparser.misc.anchortaginfo import AnchorTagInfo


class HtmlOp:
    @classmethod
    def get_anchor_under_b(cls, child, cond=None):
        if cond is None:
            list = child.find_all("b")
        else:
            list = child.find_all("b", cond)
        assoc_array = [cls.get_anchor_all(b_tag) for b_tag in list]

        return assoc_array

    @classmethod
    def get_anchor_all(cls, child):
        return [
            cls.get_anchor_tag_info(anchor_tag) for anchor_tag in child.find_all("a")
        ]

    @classmethod
    def get_anchor_tag_info(cls, anchor_tag):
        if anchor_tag is None:
            return None

        # print('----')
        a_tag_info = AnchorTagInfo(anchor_tag)

        return a_tag_info

    @classmethod
    def get_anchor_under_div(cls, child, cond=None):
        if cond is None:
            list = child.find_all("div", cond)
        else:
            list = child.find_all("div")

        for div_tag in list:
            print(f"get_anchor_under_div div_tag: {div_tag}")
            anchor_tag_info_array = HtmlOp.get_anchor_all(div_tag)
            for anchor_tag_info in anchor_tag_info_array:
                cls.print_tag_info(anchor_tag_info)

    @classmethod
    def print_tag_info(cls, assoc):
        tag = assoc["tag"]
        print(tag)

        mes_array = assoc["mes_array"]
        mes = "\n".join(mes_array)
        print(mes)
