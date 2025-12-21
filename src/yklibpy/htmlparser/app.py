import sys
from pathlib import Path
from typing import List

# from .ascraper import AScraper
from .ascraper import AScraper
from ..common.env import Env
from .h3scraper import H3Scraper
from .kuscraper import KUScraper
from .fanzadoujinscraper import FanzaDoujinScraper
from .fanzadoujinboughtscraper import FanzaDoujinBoughtScraper
from .scraper import Scraper

# from progress import Progress
from .udemyscraper import UdemyScraper

class App:
    """
    HTMLファイルからリンクを抽出するアプリケーションクラス
    """

    def __init__(self):
        """Reset link buffers, metadata, and counters for a fresh run.

        Returns:
            None
        """
        self.links_list = []
        self.links_assoc = {}
        self.info = {}
        self.append_count = 0
        self.no_append_count = 0

    def create_scraper(self, mode: str) -> Scraper:
        """Build the appropriate scraper implementation for the requested mode.

        Args:
            mode (str): Logical identifier such as ``"udemy"`` or ``"h3"``.

        Returns:
            Scraper: Concrete scraper that knows how to parse the given site, or
            ``None`` when the mode is unsupported.
        """
        if mode == "udemy":
            return UdemyScraper()
            # return H3Scraper()
            # return AScraper()
        elif mode == "h3":
            return H3Scraper()
        elif mode == "a":
            return AScraper()
        elif mode == "ku":
            return KUScraper()
        elif mode == "fanza_doujin":
            return FanzaDoujinScraper()
        elif mode == "fanza_doujin_bought":
            return FanzaDoujinBoughtScraper()
        else:
            return None

    def loop(self, files: List[Path], mode: str):
        """Iterate through HTML files and accumulate extracted link metadata.

        Args:
            files (List[Path]): Collection of HTML paths to inspect.
            mode (str): Scraper mode passed through to :meth:`create_scraper`.

        Returns:
            dict: Mapping of link identifiers to their structured attributes.
        """
        assoc = {}
        for file in files:
            print(f"file={file}")
            scraper = self.create_scraper(mode)
            extracted_links_assoc = scraper.get_links_assoc_from_html(file)
            if extracted_links_assoc:
                # print(f"app.py loop Found {len(extracted_links_assoc)} links in '{file}':\n")
                # arrayx = scraper.get_link_array(extracted_links)
                # print(f'app.py loop len(arrayx)={len(arrayx)}')
                if len(extracted_links_assoc) > 0:
                    print(f"run len( extracted_links_assoc )={len(extracted_links_assoc)}")
                    assoc.update(extracted_links_assoc)
        print(f"app.loop TOTAL len( assoc )={len(assoc)}")
        return assoc

    def run(self, env: Env):
        """Fetch file paths from the environment and scrape each one.

        Args:
            env (Env): Environment descriptor that supplies file lists and mode.

        Returns:
            None
        """
        path_array = env.get_files()
        mode = env.mode()

        assoc = self.loop(path_array, mode)
        print(f"app.py run len( assoc )={len(assoc)}")
        # self.links_assoc = self.links_assoc.update(list)
        self.links_assoc.update(assoc)
        print(f"app.py run len( self.links_assoc )={len(self.links_assoc)}")

if __name__ == "__main__":
    ymain()
