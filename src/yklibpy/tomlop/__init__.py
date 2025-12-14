from .tomlop import Tomlop


def xmain() -> str:
    print("Hello from yklibpy!")
    return "Hello from yklibpy!"

def ymain() -> str:
    print("Y Hello from yklibpy!")
    return "Y Hello from yklibpy!"

__all__ = [
    "Tomlop",
]

if __name__ == "__main__":
    xmain()
