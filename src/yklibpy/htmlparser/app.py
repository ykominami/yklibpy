import sys
from pathlib import Path
from typing import List

# from .ascraper import AScraper
from .ascraper import AScraper
from ..common.env import Env
from .h3scraper import H3Scraper
from .kuscraper import KUScraper
from .scraper import Scraper

# from progress import Progress
from .udemyscraper import UdemyScraper
from ..common.util import Util
from ..common.topconfig import TopConfig

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

def ymain():
    input_file_path = None
    input_file = sys.argv[1] if len(sys.argv) > 1 else None

    cmd_file = sys.argv[1] if len(sys.argv) > 1 else "cmd.yaml"
    cmd_file_path = Path(cmd_file)
    top_config = TopConfig(cmd_file_path)
    env = top_config.get_env()
    patterns = top_config.get_patterns()

    if input_file is None:
        input_file = top_config.get_input_file_name() 

    if input_file is not None:
        input_file_path = Path(input_file)     

    app = App()
    if input_file_path is not None and input_file_path.exists():
        input_assoc = Util.load_yaml(input_file_path)
        app.links_assoc.update(input_assoc)

    for pattern in patterns:
        print("app.py main pattern={pattern}")
        ret = env.set_pattern(pattern)
        if ret is None:
            print(f"Not found pattern={pattern}")
            exit(0)
        app.run(env)

    output_file = top_config.get_output_file_name()
    print(f'output_file={output_file}')
    output_path = Path(output_file)
    Util.output_yaml(app.links_assoc, output_path)
    
    return 100

if __name__ == "__main__":
    ymain()
