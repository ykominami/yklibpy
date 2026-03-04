class SafeDict(dict[str, str]):
    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"
