from bs4.element import Tag


class Tagx:
    def __init__(self, tag: Tag, namex: str):
        self.tag = tag
        self.strx = str(tag)
        self.type = type(tag)
        self.mes_type = f"  type({namex}): {str(type(namex))}"
        if hasattr(tag, "get_text"):
            self.text = tag.get_text(strip=True)
            self.mes_text = f"  {namex}_text: {self.text}"
        else:
            self.mes_text = f"  {namex}_text: [Nothing]"

        if hasattr(tag, "name"):
            self.mes_name = f"  {namex}.name: {tag.name}"
            # print()
        else:
            self.mes_name = f"  {namex}.name: [Nothing]"

    def set_option(self, option):
        self.option = option

    def get_option(self):
        return self.option
