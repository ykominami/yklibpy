from pathlib import Path
from typing import List

from yklibpy.common.env import Env
from yklibpy.htmlparser.amazonsavedcartscraper import AmazonSavedCartScraper
from yklibpy.htmlparser.fanzadoujinbasketscraper import FanzaDoujinBasketScraper
from yklibpy.htmlparser.fanzadoujinpurchasedscraper import FanzaDoujinPurchasedScraper
from yklibpy.htmlparser.kuscraper import KUScraper
from yklibpy.htmlparser.scraper import Scraper
from yklibpy.htmlparser.udemyscraper import UdemyScraper


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

    def create_scraper(self, mode: str, sequence: int) -> Scraper | None:
        """Build the appropriate scraper implementation for the requested mode.

        Args:
            mode (str): Logical identifier such as ``"udemy"`` or ``"h3"``.

        Returns:
            Scraper: Concrete scraper that knows how to parse the given site, or
            ``None`` when the mode is unsupported.
        """
        print(f"mode={mode}")
        if mode == "udemy":
            return UdemyScraper(sequence)
            # return H3Scraper()
            # return AScraper()
        elif mode == "ku":
            return KUScraper(sequence)
        elif mode == "fanza_doujin_basket":
            return FanzaDoujinBasketScraper(sequence)
        elif mode == "fanza_doujin_purchased":
            return FanzaDoujinPurchasedScraper(sequence)
        elif mode == "amazon_saved_cart":
            # print(f'mode={mode}')
            return AmazonSavedCartScraper(sequence)
        else:
            print(f"mode={mode} is not supported")
            return None

    def loop(self, files: List[Path], mode: str, sequence: int):
        """Iterate through HTML files and accumulate extracted link metadata.

        Args:
            files (List[Path]): Collection of HTML paths to inspect.
            mode (str): Scraper mode passed through to :meth:`create_scraper`.

        Returns:
            dict: Mapping of link identifiers to their structured attributes.
        """
        print(f"S loop files={files}")
        assoc: dict[str, dict[str, str]] = {}
        for file in files:
            scraper: Scraper | None = self.create_scraper(mode, sequence)
            if scraper is None:
                continue
            extracted_links_assoc = scraper.get_links_assoc_from_html(file)
            if extracted_links_assoc:
                len_extracted_links_assoc = len(extracted_links_assoc)
                if len_extracted_links_assoc > 0:
                    len_assoc = len(assoc)
                    print(f"0 len_assoc={len_assoc}")
                    assoc.update(extracted_links_assoc)
                    print(f"1 len_assoc={len(assoc)}")
                else:
                    print(f"3 len_extracted_links_assoc={len_extracted_links_assoc}")
            else:
                print(f"4 extracted_links_assoc={extracted_links_assoc}")
        return assoc

    def run(self, env: Env):
        """Fetch file paths from the environment and scrape each one.

        Args:
            env (Env): Environment descriptor that supplies file lists and mode.

        Returns:
            None
        """
        path_array = env.get_files()
        sequence = env.sequence
        message = f"path_array={path_array} sequence={sequence}"
        # raise Exception(message)
        print(message)

        mode = env.mode()

        assoc = self.loop(path_array, mode, sequence)
        self.links_assoc.update(assoc)
