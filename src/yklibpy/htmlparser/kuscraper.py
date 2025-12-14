from typing import Dict, List
from urllib.parse import urlparse

from ..common.info import Info
from .scraper import Scraper


class KUScraper(Scraper):
    def __init__(self):
        super().__init__()

    def scrape(self, info: Info) -> List[Dict[str, str]]:
        print("kuscraper scrape")
        soup = info.soup
        """aの処理"""
        for a_tag in soup.find_all("a"):
            # classが"a-link-normal"でない場合はcontinue
            if a_tag.get("class") != ["a-link-normal"]:
                # print(f'a_tag.get("class")={a_tag.get("class")} not a-link-normal')
                continue
            # print(f'a_tag.get("class")={a_tag.get("class")} a-link-normal')
            url = a_tag.get("href", "#")
            # print(f'url={url}')
            img_tag = a_tag.find("img")
            # print(f'img_tag={img_tag}')
            if img_tag:
                text = img_tag.get("alt", "")
            else:
                text = a_tag.get_text(strip=True)
            # print(f'text={text}')
            self.add_list_and_assoc(url=url, text=text)
        return self.links_list

    def add_list_and_assoc(
        self, url: str, text: str
    ) -> bool:
        """Insert a new record if the ``course_id`` has not been seen.

        Args:
            url (str): Course URL.
            text (str): Anchor text/label.

        Returns:
            bool: ``True`` when the record was added, else ``False``.
        """
        result = False
        if url not in self.links_assoc.keys():
            record = self.make_record(
                url=url, text=text
            )
            # record = self.make_record(url, text, course_id)
            # print(f'=1 record1={record}')

            self.links_assoc[url] = record
            self.links_list.append(record)
            result = True
        else:
            pass

        return result

    def make_record(
        self, url: str, text: str
    ) -> Dict[str, str]:
        """Construct the normalized record stored in outputs.

        Args:
            url (str): Course URL, must be valid.
            text (str): Display name.

        Returns:
            Dict[str, str]: Record containing URL/Text/Course_ID/Instructors/Progress.

        Raises:
            ValueError: If the supplied URL lacks a scheme or structure.
        """
        """レコードを作成する"""
        # URI形式のチェック
        parsed = urlparse(url)
        if not parsed.scheme:
            raise ValueError(f"URL '{url}' is not a valid URI: missing scheme")
        if not parsed.netloc and not parsed.path and not parsed.fragment:
            raise ValueError(f"URL '{url}' is not a valid URI: missing authority, path, or fragment")
        # progress_yml = progress.to_yml()
        record = {
            "URL": url,
            "Text": text,
        }
        # print(f'0 record0={record}')
        return record

