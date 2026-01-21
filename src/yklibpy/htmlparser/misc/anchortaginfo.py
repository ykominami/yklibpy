from yklibpy.htmlparser.misc.anchortagx import AnchorTagx
from yklibpy.htmlparser.misc.tagx import Tagx
from typing import Optional
from bs4.element import PageElement


class AnchorTagInfo:
    def __init__(self, anchor_tag: Optional[PageElement]):
        self.anchor = AnchorTagx(anchor_tag)
        self.parent_parent: Optional[Tagx] = None
        self.parent: Optional[Tagx] = None
        self.next_sibling: Optional[Tagx] = None

    def setup(self):
        # print()
        if self.anchor.tag is not None:
            self.next_sibling = Tagx(self.anchor.tag.next_sibling, "next_sibling")
            self.parent = Tagx(self.anchor.tag.next_sibling, "parent")
            if self.anchor.tag.parent is not None:
                self.parent_parent = Tagx(self.anchor.tag.parent.parent, "parent.parent")
            else:
                self.parent_parent = None
        else:
            self.next_sibling = None
            self.parent = None
            self.parent_parent = None
