from .app import App
from .ascraper import AScraper
from .h3scraper import H3Scraper
from .kuscraper import KUScraper
from .progress import Progress
from .scraper import Scraper
from .udemyscraper import UdemyScraper


def xmain() -> str:
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"

def ymain() -> str:
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"

__all__ = [
    "App",
    "AScraper",
    "H3Scraper",
    "KUScraper",
    "Progress",
    "Scraper",
    "UdemyScraper",
]

if __name__ == "__main__":
    xmain()
