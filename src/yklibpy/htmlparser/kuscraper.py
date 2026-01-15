from typing import Dict, List

from ..common.info import Info
from ..common.util import Util
from .scraper import Scraper


class KUScraper(Scraper):
    class WorkInfo:
        def __init__(self, url: str, title: str):
            result = Util.isValidUrls([url])
            if result:
                self.url = url
                self.title = title
            else:
                self.url = None
                self.title = None

        def to_assoc(self):
            return {
                "url": self.url,
                "titlet": self.title,
            }

    def __init__(self):
        super().__init__()

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        # <div id="itemsList" class="a-section a-spacing-top-large">
        #   <ul id="listContainer" class="a-unordered-list a-nostyle a-vertical" role="list">

        soup = info.soup
        """aの処理"""
        for div_tag in soup.find_all("div", {"id": "itemsList"}):
            for a_tag in div_tag.find_all("a"):
                if a_tag.get("class") != ["a-link-normal"]:
                    continue
                url = a_tag.get("href", "#")
                img_tag = a_tag.find("img")
                if img_tag:
                    title = img_tag.get("alt", "")
                else:
                    title = a_tag.get_text(strip=True)
                # print(f"text={text}")
                work_info = self.WorkInfo(url=url, title=title)
                self.add_list_and_assoc(work_info)
        return self.links_list

    def add_list_and_assoc(self, work_info: WorkInfo) -> bool:
        """Insert a new record if the ``course_id`` has not been seen.

        Args:
            url (str): Course URL.
            text (str): Anchor text/label.

        Returns:
            bool: ``True`` when the record was added, else ``False``.
        """
        result = False
        if work_info.url not in self.links_assoc.keys():
            self.links_assoc[work_info.url] = work_info.to_assoc()
            self.links_list.append(work_info)
            result = True
        else:
            pass

        return result
