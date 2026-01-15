from typing import Dict, List

from bs4.element import NavigableString

from ..common.info import Info
from ..common.util import Util
from .scraper import Scraper


class AmazonSavedCartScraper(Scraper):
    class WorkInfo:
        def __init__(self, asin: str, target: str, url: str, title: str):
            self.asin = asin
            self.target = target
            self.title = title

            result = Util.isValidUrls([url])
            if result:
                self.url = url
            else:
                self.url = None

        def to_assoc(self):
            return {
                "asin": self.asin,
                "target": self.target,
                "url": self.url,
                "title": self.title,
            }

    def __init__(self):
        """Initialize Udemy-specific scraper state.

        Returns:
          None
        """
        super().__init__()

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        """Extract Udemy dashboard cards and convert them into records.

        Args:
          info (Info): Parsed HTML container and counters for the current file.

        Returns:
          List[Dict[str, str]]: List of record dictionaries appended this run.
        """
        print("amazonsavedcart scrape")
        soup = info.soup
        append_count = 0
        no_append_count = 0
        """divの処理"""
        print("--- 子要素の列挙 ---")

        for div_tag in soup.find_all("div", {"id": "sc-saved-cart-items"}):
            # print(div_tag)
            list = div_tag.find_all("div", {"data-asin": True})
            # print(list)
            for div_tag_2 in list:
                # print(f'div_tag_2={div_tag_2}')
                asin = div_tag_2.get("data-asin", "")
                # print(f'asin={asin}')
                div_tag_3 = div_tag_2.find("div", {"class": "sc-list-item-removed-msg"})
                # print(f"div_tag_3={div_tag_3}")
                if div_tag_3 is not None:
                    a_tag = div_tag_2.find("a")
                    if a_tag is None:
                        continue
                    url = a_tag.get("href", "#")
                    title = "".join(
                        s for s in a_tag.contents if isinstance(s, NavigableString)
                    ).strip()
                    # course_id = self.get_course_id_from_url(url)
                    # print(f'asin={asin}')
                    # print(f'url={url}')
                    # print(f'text={text}')
                    # print("====")
                    work_info = self.WorkInfo(
                        asin=asin, target="savedcart", url=url, title=title
                    )
                    result = self.add_list_and_assoc(work_info)

                    if result:
                        append_count += 1
                    else:
                        no_append_count += 1

        print("--- 子要素の列挙終了 ---")

        info.append_count = append_count
        info.no_append_count = no_append_count
        self.append_count += append_count
        self.no_append_count += no_append_count
        print(
            f"###############   amazonsavedcart scrape len( self.links_list )={len(self.links_list)}"
        )
        print(
            f"###############   amazonsavedcart scrape len( self.links_assoc )={len(self.links_assoc)}"
        )
        return self.links_list

    def add_list_and_assoc(self, work_info: WorkInfo) -> bool:
        result = False
        if work_info.asin not in self.links_assoc.keys():
            self.links_assoc[work_info.asin] = work_info
            self.links_list.append(work_info)
            result = True
        else:
            pass

        return result
