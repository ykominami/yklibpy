from yklibpy.common.loggerx import Loggerx
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
    Loggerx.debug("Hello from yklibpy!", __name__)
    return "Hello from yklibpy!"


def ymain() -> str:
    """HTML パーサパッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy!", __name__)
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
