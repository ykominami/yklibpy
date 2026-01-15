# from .htmlparser import htmlparser
# from .common import common
# from .tomlop import tomlop
from .db import db_yaml

__all__ = ["db_yaml"]


def dbyaml():
    db_yaml()


def xmain() -> str:
    print("11 Hello from yklibpy.xmain!")
    return "12 Hello from yklibpy.xmain!"


def ymain() -> str:
    print("21 Y Hello from yklibpy.ymain!")
    return "22 Y Hello from yklibpy.ymain!"
