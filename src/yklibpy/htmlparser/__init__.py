from yklibpy.htmlparser.app import App
from yklibpy.htmlparser.preparex import Preparex
from yklibpy.htmlparser.progress import Progress
from yklibpy.htmlparser.scraper import Scraper
from yklibpy.htmlparser.htmlop import HtmlOp

__all__ = [
    "App",
    "Progress",
    "Scraper",
    "Preparex",
    "HtmlOp",
]


def xmain() -> str:
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"


def ymain() -> str:
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
