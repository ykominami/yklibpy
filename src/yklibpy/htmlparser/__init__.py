from yklibpy.htmlparser.amazonsavedcartscraper import AmazonSavedCartScraper
from yklibpy.htmlparser.app import App
from yklibpy.htmlparser.fanzadoujinpurchasedscraper import FanzaDoujinPurchasedScraper
from yklibpy.htmlparser.fanzadoujinbasketscraper import FanzaDoujinBasketScraper
from yklibpy.htmlparser.kuscraper import KUScraper
from yklibpy.htmlparser.preparex import Preparex
from yklibpy.htmlparser.progress import Progress
from yklibpy.htmlparser.scraper import Scraper
from yklibpy.htmlparser.udemyscraper import UdemyScraper
from yklibpy.htmlparser.htmlop import HtmlOp

__all__ = ["App", "AmazonSavedCartScraper", "FanzaDoujinPurchasedScraper", "FanzaDoujinBasketScraper", "KUScraper", "Progress", "Scraper", "UdemyScraper", "HtmlOp"]

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
    "FanzaDoujinBasketScraper",
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
