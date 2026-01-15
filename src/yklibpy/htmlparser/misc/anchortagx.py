from .tagx import Tagx


class AnchorTagx(Tagx):
    def __init__(self, anchor_tag):
        super().__init__(anchor_tag, "anchor")
        self.href = self.tag.get("href", "")
        self.text = self.tag.get_text(strip=True)
        self.mes_href = f"  href: {self.href}"
        self.mes_text = f"  text: {self.text}"

    def show(self):
        return "\n".join([self.href, self.text])
