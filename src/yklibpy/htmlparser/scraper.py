from pathlib import Path
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup

from yklibpy.common.info import Info
from yklibpy.common.util import Util


class Scraper:
    def __init__(self, sequence: int):
        """Initialize in-memory containers for links and bookkeeping.

        Returns:
          None
        """
        self.sequence = sequence
        self.links_assoc: dict[str, dict[str, Any]] = {}
        self.info: dict[str, Info] = {}
        self.append_count = 0
        self.no_append_count = 0

    @classmethod
    def _to_assoc(cls, title: str, url: str, sequence: int):
        return {"title": title, "url": url, "sequence_array": set([sequence])}

    @classmethod
    def _add_assoc(
        cls,
        links_assoc: dict[str, dict[str, Any]],
        key: str,
        sequence: int,
        value_dict: dict[str, Any],
    ) -> bool:
        result = False
        link = links_assoc.get(key, None)
        if link is None:
            links_assoc[key] = value_dict
            result = True
        else:
            link["sequence_array"].add(sequence)
            # raise ValueError(f"link is not None: {link}")
        return result

    def _extract_links_assoc_from_info(self, info: Info) -> Dict[str, Dict[str, Any]]:
        """Populate the associative map keyed by course ID.

        Args:
          info (Info): Parsed HTML payload for a file.

        Returns:
          dict: ``links_assoc`` containing course records.
        """
        self.scrape(info)
        return self.links_assoc

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

    def scrape(self, info: Info):
        """Primary scraping entry point; implemented by subclasses.

        Args:
          url (str): Resource identifier or file hint.

        Returns:
          None
        """
        pass

    def get_links_assoc_from_html(self, file_path: Path) -> Dict[str, Dict[str, Any]]:
        """Parse an HTML file and return the associative course map.

        Args:
            file_path (Path): Location of the HTML snapshot.

        Returns:
            dict: ``links_assoc`` entries derived from the file.
        """
        assoc = {}
        if file_path.name not in self.info.keys():
            soup = self._parse_html_file(file_path)
            if soup:
                info = Info(file_path, file_path.name, soup, 0, 0)
                self.info[file_path.name] = info
                assoc = self._extract_links_assoc_from_info(info)
        return assoc
