from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

from ..common.info import Info
from ..common.util import Util


class Scraper:
    def __init__(self):
        """Initialize in-memory containers for links and bookkeeping.

        Returns:
          None
        """
        self.links_list = []
        self.links_assoc = {}
        self.info = {}
        self.append_count = 0
        self.no_append_count = 0

    def _extract_links_assoc_from_info(self, info: Info) -> List[Dict[str, str]]:
        """Populate the associative map keyed by course ID.

        Args:
          info (Info): Parsed HTML payload for a file.

        Returns:
          dict: ``links_assoc`` containing course records.
        """
        self.scrape(info)
        return self.links_assoc

    def _extract_links_from_info(self, info: Info) -> List[Dict[str, str]]:
        """Base stub that child classes override to populate ``links_list``.

        Args:
          info (Info): Parsed HTML context for the current file.

        Returns:
          List[Dict[str, str]]: Defaults to an empty list.
        """
        self.links_list = []
        return self.links_list

    def _parse_html_file(self, file_path: Path) -> Optional[BeautifulSoup]:
        """Read an HTML file and parse it into BeautifulSoup.

        Args:
            file_path (Path): Path to the HTML file on disk.

        Returns:
            BeautifulSoup | None: Parsed DOM on success, otherwise ``None`` when
            the file is missing or parsing fails.
        """
        try:
            encoding = Util.detect_encoding(file_path)
            if encoding is None:
                encoding = "utf-8"

            with file_path.open("r", encoding=encoding) as f:
                # Create a BeautifulSoup object using the lxml parser
                # soup = BeautifulSoup(f, 'lxml')
                soup = BeautifulSoup(f, "html5lib")
                return soup
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def scrape(self, url: str):
        """Primary scraping entry point; implemented by subclasses.

        Args:
          url (str): Resource identifier or file hint.

        Returns:
          None
        """
        pass

    def get_links_assoc_from_html(self, file_path: Path) -> List[Dict[str, str]]:
        """Parse an HTML file and return the associative course map.

        Args:
            file_path (Path): Location of the HTML snapshot.

        Returns:
            dict: ``links_assoc`` entries derived from the file.
        """
        assoc = {}
        if file_path not in self.info.keys():
            soup = self._parse_html_file(file_path)
            if soup:
                info = Info(file_path, file_path.name, soup, 0, 0)
                self.info[file_path.name] = info
                assoc = self._extract_links_assoc_from_info(info)
        return assoc

    def get_links_from_html(self, file_path: Path) -> List[Dict[str, str]]:
        """Parse an HTML file and return a list of course records.

        Args:
            file_path (Path): Location of the HTML snapshot.

        Returns:
            List[Dict[str, str]]: Extracted course entries.
        """
        links = []
        if file_path not in self.info.keys():
            soup = self._parse_html_file(file_path)
            if soup:
                info = Info(file_path, file_path.name, soup, 0, 0)
                self.info[file_path.name] = info
                links = self._extract_links_from_info(info)
        return links

    def _extract_links_from_info(self, info: Info) -> List[Dict[str, str]]:
        links_list = self.scrape(info)
        return links_list

    def find_status_span_ancestors(self, soup: BeautifulSoup):
        """Locate role=\"status\" spans and dump their ancestor structure.

        Args:
            soup (BeautifulSoup): Parsed HTML document.

        Returns:
            list: Result from :meth:`find_item_ancestors`.
        """
        status_spans = soup.find_all("span", role="status")
        return self.find_item_ancestors(status_spans)

    def find_item_ancestors(self, items: List[Dict[str, any]]):
        """Traverse ancestor chains for the supplied elements and log details.

        Args:
            items (List[Dict[str, any]]): Result set (e.g., BeautifulSoup nodes)
                whose parent hierarchy should be inspected.

        Returns:
            list: Currently an empty list placeholder for future aggregation.
        """
        for i, item in enumerate(items, 1):
            # 祖先要素をすべて取得
            ancestors = []
            current = item.parent
            level = 1

            while current and current.name != "html":
                assoc = {
                    "level": level,
                    "tag": current.name,
                    "text": current.get_text(strip=True)[:100] + "..."
                    if len(current.get_text(strip=True)) > 100
                    else current.get_text(strip=True),
                    "class": current.get("class", []),
                    "id": current.get("id", ""),
                }
                ancestors.append(assoc)
                if "item" in assoc["class"]:
                    break

                current = current.parent
                level += 1

            """
            for ancestor in ancestors:
                indent = "  " * ancestor["level"]
                print(f"{indent}Level {ancestor['level']}: <{ancestor['tag']}>")
                print(f"{indent}  Text: {ancestor['text']}")
                print(f"{indent}  Class: {ancestor['class']}")
                print(f"{indent}  ID: {ancestor['id']}")

            print("-" * 50)
            """

        return []
