from typing import Dict, List
from urllib.parse import urlparse

from ..common.info import Info
from .scraper import Scraper


class FanzaDoujinBoughtScraper(Scraper):
    def __init__(self):
        super().__init__()

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        print("FanzaDoujin scrape")
        soup = info.soup
        append_count = 0
        no_append_count = 0
        for div_tag in soup.find_all("div", {"id": "doujinBasket"}):
            print(div_tag)
            # div_tagの子要素を列挙して表示
            print("--- 子要素の列挙 ---")
            for idx, child in enumerate(div_tag.children, 1):
                print(f"子要素 {idx}: {child}")
            print("--- 子要素の列挙終了 ---")

    def scrape0(self, info: Info) -> List[Dict[str, str]]:
        """Extract Udemy dashboard cards and convert them into records.

        Args:
          info (Info): Parsed HTML container and counters for the current file.

        Returns:
          List[Dict[str, str]]: List of record dictionaries appended this run.
        """
        print("FanzaDoujin scrape")
        soup = info.soup
        append_count = 0
        no_append_count = 0
        """divの処理"""
        for div_tag in soup.find_all("div", {"class": "enrolled-course-card--container--WJYo9"}):
            # print(f'div_tag={div_tag}')
            a_tag = div_tag.find("a")
            if a_tag is None:
                continue
            url = a_tag.get("href", "#")
            text = a_tag.get_text(strip=True)
            course_id = self.get_course_id_from_url(url)

            instructors = self.get_instructors(div_tag)
            progress = self.get_progress(div_tag)

            # Extract course_id from URL parameters

            result = self.add_list_and_assoc(
                url=url, text=text, course_id=course_id, instructors=instructors, progress=progress
            )
            if result:
                append_count += 1
            else:
                no_append_count += 1

        info.append_count = append_count
        info.no_append_count = no_append_count
        self.append_count += append_count
        self.no_append_count += no_append_count
        print(f"###############   udemyscraper scrape len( self.links_list )={len(self.links_list)}")
        print(f"###############   udemyscraper scrape len( self.links_assoc )={len(self.links_assoc)}")
        return self.links_list

