from yklibpy.common.env import Env
from yklibpy.common.info import Info
from yklibpy.common.util import Util
from yklibpy.common.util_yaml import UtilYaml
from yklibpy.common.util_json import UtilJson
from yklibpy.common.safedict import SafeDict
from yklibpy.common.timex import Timex

__all__ = ["Env", "Info", "Util", "UtilYaml", "UtilJson", "SafeDict", "Timex"]


def xmain() -> str:
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"


def ymain() -> str:
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
