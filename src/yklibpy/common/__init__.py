from yklibpy.common.env import Env
from yklibpy.common.info import Info
from yklibpy.common.loggerx import Loggerx
from yklibpy.common.opresult import OpResult
from yklibpy.common.safedict import SafeDict
from yklibpy.common.timex import Timex
from yklibpy.common.util import Util
from yklibpy.common.util_json import UtilJson
from yklibpy.common.util_yaml import UtilYaml

__all__ = ["Env", "Info", "OpResult", "SafeDict", "Timex", "Util", "UtilJson", "UtilYaml"]


def xmain() -> None:
    """common パッケージの動作確認を行う。

    ログ出力で疎通確認できるようにする。
    """
    Loggerx.debug("Hello from yklibpy!", __name__)


def ymain() -> None:
    """common パッケージの別系統の確認を行う。

    エントリポイントの差し替えや簡易確認で使うことを想定する。
    """
    Loggerx.debug("Y Hello from yklibpy!", __name__)


if __name__ == "__main__":
    xmain()
