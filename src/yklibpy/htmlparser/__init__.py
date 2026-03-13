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
    """HTML パーサパッケージの疎通確認用メッセージを返す。"""
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"


def ymain() -> str:
    """HTML パーサパッケージの別系統の疎通確認用メッセージを返す。"""
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
