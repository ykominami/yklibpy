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


def xmain() -> None:
    """HTML パーサパッケージの疎通確認を行う。"""
    Loggerx.debug("Hello from yklibpy!", __name__)


def ymain() -> None:
    """HTML パーサパッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy!", __name__)


if __name__ == "__main__":
    xmain()
