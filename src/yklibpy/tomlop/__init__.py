from yklibpy.common.loggerx import Loggerx
from yklibpy.tomlop.fileitem import FileItem
from yklibpy.tomlop.tomlop import Tomlop, toml2yaml, yaml2toml, zmain

__all__ = [
    "Tomlop",
    "FileItem",
    "zmain",
    "toml2yaml",
    "yaml2toml",
    "xmain",
    "ymain",
]


def xmain() -> None:
    """tomlop パッケージの疎通確認用メッセージを返す。"""
    msg = "Hello from yklibpy.tomlop!"
    print(msg)
    Loggerx.debug(msg, __name__)


def ymain() -> None:
    """tomlop パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.tomlop!", __name__)


if __name__ == "__main__":
    xmain()
