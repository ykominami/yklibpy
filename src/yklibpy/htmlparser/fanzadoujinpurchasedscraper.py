from typing import Dict, List

from ..common.info import Info
from ..common.util import Util
from .scraper import Scraper


class FanzaDoujinPurchasedScraper(Scraper):
    class WorkInfo:
        def __init__(
            self,
            target: str,
            product_id: str,
            url: str,
            purchased_date: str,
            kind: str,
            title: str,
            circle_name: str,
        ):
            self.target = target
            self.product_id = product_id
            self.url = url
            self.purchased_date = purchased_date
            self.kind = kind
            self.title = title
            self.circle_name = circle_name

        def to_assoc(self):
            return {
                "product_id": self.product_id,
                "target": self.target,
                "url": self.url,
                "purchased_date": self.purchased_date,
                "kind": self.kind,
                "title": self.title,
                "circle_name": self.circle_name,
            }

    def __init__(self):
        super().__init__()

    def add_list_and_assoc(self, work_info: WorkInfo):
        result = False
        if work_info.product_id not in self.links_assoc.keys():
            self.links_assoc[work_info.product_id] = work_info.to_assoc()
            self.links_list.append(work_info.to_assoc())
            result = True
        else:
            pass

        return result

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        soup = info.soup
        append_count = 0
        no_append_count = 0
        id_str = "mylibrary-app"
        target = "purchased"
        for top in soup.find_all("div", {"id": id_str}):
            for purchased_date in top.find_all(
                "p", {"class": "purchasedListTitleiBWYR"}
            ):
                purchased_date_text = purchased_date.text
                parent = purchased_date.parent
                for div_tag in parent.find_all(
                    "div", {"class": "localListProductzKID2"}
                ):
                    anchor_tag = div_tag.find("a")
                    url = anchor_tag.get("href", "")
                    product_id = Util.extract_base("product_id", url)
                    span_tag = anchor_tag.find("span", {"class": "defaultClassmE6be"})
                    kind = span_tag.text
                    namex = anchor_tag.find("div", {"class": "productTitleCMVya"})
                    title = namex.text
                    p_tag = anchor_tag.find("p", {"class": "circleNameGWNom"})
                    circle_name = p_tag.text
                    work_info = self.WorkInfo(
                        target=target,
                        url=url,
                        product_id=product_id,
                        purchased_date=purchased_date_text,
                        kind=kind,
                        title=title,
                        circle_name=circle_name,
                    )
                    result = self.add_list_and_assoc(work_info)
                    if result:
                        append_count += 1
                    else:
                        no_append_count += 1

        info.append_count = append_count
        info.no_append_count = no_append_count
        self.append_count += append_count
        self.no_append_count += no_append_count
        return self.links_list
