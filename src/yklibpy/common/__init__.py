from .env import Env
from .info import Info
from .util import Util

def xmain() -> str:
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"

def ymain() -> str:
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"


if __name__ == "__main__":
    xmain()
