from .amazonsavedcartscraper import AmazonSavedCartScraper
from .app import App
from .ascraper import AScraper
from .fanzadoujinpurchasedscraper import FanzaDoujinPurchasedScraper
from .fanzadoujinscraper import FanzaDoujinScraper
from .h3scraper import H3Scraper
from .kuscraper import KUScraper
from .preparex import Preparex
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
    "AmazonSavedCartScraper",
    "AScraper",
    "FanzaDoujinPurchasedScraper",
    "FanzaDoujinScraper",
    "FanzaDoujindScraper",
    "H3Scraper",
    "KUScraper",
    "Progress",
    "Scraper",
    "UdemyScraper",
    "Preparex",
]

if __name__ == "__main__":
    xmain()
