from typing import Dict, List

from ..common.info import Info
from ..common.util import Util
from .htmlop import HtmlOp
from .scraper import Scraper


class FanzaDoujinScraper(Scraper):
    class WorkInfo:
        def __init__(
            self,
            target: str,
            url: str,
            title: str,
            maker_url: str,
            maker_text: str,
            creator_url: str,
            creator_text: str,
            price_old: str,
            price_real: str,
        ):
            self.target = target
            self.title = title
            self.maker_text = maker_text
            self.creator_text = creator_text
            self.price_old = price_old
            self.price_real = price_real

            result_array = Util.isValidUrls([url, maker_url, creator_url])
            if result_array[0].success:
                self.url = url
            else:
                self.url = None

            if result_array[1].success:
                self.maker_url = maker_url
            else:
                self.url = None

            if result_array[2].success:
                self.creator_url = creator_url
            else:
                self.creator_url = None

        def to_assoc(self):
            return {
                "target": self.target,
                "url": self.url,
                "title": self.title,
                "maker_url": self.maker_url,
                "maker_text": self.maker_text,
                "creator_url": self.creator_url,
                "creator_text": self.creator_text,
                "price_old": self.price_old,
                "price_real": self.price_real,
            }

    def __init__(self):
        super().__init__()

    def get_anchor_under_p(self, child, cond=None):
        # div basket-txtContent
        #  b basket-name
        #  p basket-circle
        if cond is None:
            list = child.find_all("p")
        else:
            list = child.find_all("p", cond)
        # print(f"get_anchor_under_p list={list}")
        # print(f"child={child}")

        assoc_array = [HtmlOp.get_anchor_all(p_tag) for p_tag in list]

        return assoc_array

    def get_work_maker_and_creator(self, div_tag):
        cond = {"class": "basket-circle"}
        assoc_array_p = self.get_anchor_under_p(div_tag, cond)
        assoc_p_flat = list(Util.flatten_gen(assoc_array_p))

        maker = None
        creator = None
        for as_p in assoc_p_flat:
            url = as_p.anchor.href
            result_array = Util.isValidUrls([url])
            if result_array[0].success:
                array = result_array[0].parsed.path.split("/")
                if "article=maker" in array:
                    maker = as_p
                elif "article=creator" in array:
                    creator = as_p
                else:
                    raise ValueError(
                        f"URL '{url}' is not a valid URI: missing maker or creator"
                    )

        return {"maker": maker, "creator": creator}

    def get_price_under_p(self, div_tag):
        cond = {"class": "c_txt_price"}

        p_tag = div_tag.find("p", cond)
        if p_tag is None:
            return None
        cond_span = {"class": "price-old"}

        price_old = None
        span_text = None
        span_tag = p_tag.find("span", cond_span)
        if span_tag is None:
            span_tag = p_tag.find("span")
            if span_tag:
                span_text = span_tag.text
        else:
            span_text = span_tag.text
            price_old = HtmlOp.Tagx(span_tag, "price-old")
            price_old.set_option(span_text)

        strong_tag = p_tag.find("strong")
        strong_text = strong_tag.text
        price_real = HtmlOp.Tagx(strong_tag, "price-real")
        price_real.set_option(strong_text)
        price_info = HtmlOp.PriceInfo(price_old, price_real)
        if price_old is None and price_real is None:
            raise ValueError("price_old and price_real are None")
        if price_real is None:
            raise ValueError("price_real is None")
        return price_info

    def get_work_name(self, div_tag):
        work_name = None
        cond = {"class": "basket-name"}
        assoc_array_b = HtmlOp.get_anchor_under_b(div_tag, cond)
        assoc_b_flat = list(Util.flatten_gen(assoc_array_b))
        if len(assoc_b_flat) != 1:
            cond_result = {"class": "basket-resultTxt"}
            array = div_tag.find("p", cond_result)
            if array is not None:
                len_array = list(Util.flatten_gen(array))
                if len(array) == 1:
                    return work_name
                else:
                    raise ValueError(f"Expected 1 anchor, got {len(len_array)}")
        else:
            as_b = assoc_b_flat[0]
            work_name = as_b

        return work_name

    def get_and_register_work_info(self, div_tag, target):
        self.target = target

        creator_url = ""
        creator_text = ""
        maker_url = ""
        maker_text = ""

        price_info = self.get_price_under_p(div_tag)
        if price_info is None:
            return
        price_old = price_info.get_price_old()
        price_real = price_info.get_price_real()

        work_name = self.get_work_name(div_tag)
        if work_name is None:
            return
        url = work_name.anchor.href
        title = work_name.anchor.text
        result = Util.isValidUrls([url])
        if not result:
            raise ValueError(f"URL '{url}' is not a valid URI")

        assoc = self.get_work_maker_and_creator(div_tag)
        maker = assoc["maker"]
        creator = assoc["creator"]
        maker_url = maker.anchor.href
        maker_text = maker.anchor.text
        if creator is not None:
            creator_url = creator.anchor.href
            creator_text = creator.anchor.text
        else:
            creator_url = ""
            creator_text = ""

        work_info = self.WorkInfo(
            target=target,
            url=url,
            title=title,
            maker_url=maker_url,
            maker_text=maker_text,
            creator_url=creator_url,
            creator_text=creator_text,
            price_old=price_old,
            price_real=price_real,
        )
        result = self.add_list_and_assoc(work_info)
        return result

    def add_list_and_assoc(self, work_info: WorkInfo) -> bool:
        result = False
        if work_info.url not in self.links_assoc.keys():
            cid = Util.extract_cid(work_info.url)
            self.links_assoc[cid] = work_info.to_assoc()
            self.links_list.append(work_info)
            result = True
        else:
            pass

        return result

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        print("FanzaDoujin scrape")
        soup = info.soup
        append_count = 0
        no_append_count = 0
        class_str = "c_hdg_normalWeak"
        # div_tagの子要素を列挙して表示
        print("--- 子要素の列挙 ---")
        # for div_tag in soup.find_all("div", {"id": "basket-itemContent"}):
        target = None
        for section_tag in soup.find_all("section"):
            h2_tag = section_tag.find("h2", {"class": class_str})
            if h2_tag is None:
                raise ValueError("h2_tag is None")

            h2_text = h2_tag.text
            if h2_text == "バスケット":
                target = "basket"
            elif h2_text == "「お気に入り」に入っている商品":
                target = "bookmark"
            else:
                raise ValueError(
                    "h2_tag.text is not 'バスケット' or '「お気に入り」に入っている商品'"
                )

            for div_tag in section_tag.find_all("div", {"class": "basket-itemContent"}):
                result = self.get_and_register_work_info(div_tag, target)

                if result:
                    append_count += 1
                else:
                    no_append_count += 1

        print("--- 子要素の列挙終了 ---")

        info.append_count = append_count
        info.no_append_count = no_append_count
        self.append_count += append_count
        self.no_append_count += no_append_count
        return self.links_list
