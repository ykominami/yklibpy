from yklibpy.common.env import Env
from yklibpy.common.info import Info
from yklibpy.common.loggerx import Loggerx
from yklibpy.common.util import Util
from yklibpy.common.util_yaml import UtilYaml
from yklibpy.common.util_json import UtilJson
from yklibpy.common.safedict import SafeDict
from yklibpy.common.timex import Timex

__all__ = ["Env", "Info", "Util", "UtilYaml", "UtilJson", "SafeDict", "Timex"]


def xmain() -> str:
    """`common` パッケージの動作確認用メッセージを返す。

    ログ出力と戻り値の両方で疎通確認できるようにする。
    """
    Loggerx.debug("Hello from yklibpy!", __name__)
    return "Hello from yklibpy!"


def ymain() -> str:
    """`common` パッケージの別系統の確認用メッセージを返す。

    エントリポイントの差し替えや簡易確認で使うことを想定する。
    """
    Loggerx.debug("Y Hello from yklibpy!", __name__)
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
