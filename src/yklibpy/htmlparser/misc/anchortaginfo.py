from .tagx import Tagx
from .anchortagx import AnchorTagx


class AnchorTagInfo:
    def __init__(self, anchor_tag):
        self.anchor = AnchorTagx(anchor_tag)

    def setup(self):
        # print()
        self.next_sibling = Tagx(self.anchor.tag.next_sibling, "next_sibling")
        self.parent = Tagx(self.anchor.tag.next_sibling, "parent")
        self.parent_parent = Tagx(self.anchor.tag.parent.parent, "parent.parent")
