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


def xmain() -> str:
    """tomlop パッケージの疎通確認用メッセージを返す。"""
    Loggerx.debug("Hello from yklibpy.tomlop!", __name__)
    return "Hello from yklibpy.tomlop!"


def ymain() -> str:
    """tomlop パッケージの別系統の疎通確認用メッセージを返す。"""
    Loggerx.debug("Y Hello from yklibpy.tomlop!", __name__)
    return "Y Hello from yklibpy.tomlop!"


if __name__ == "__main__":
    xmain()
