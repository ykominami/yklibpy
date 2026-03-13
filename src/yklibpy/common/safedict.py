class SafeDict(dict[str, str]):
    """未定義キーをそのままプレースホルダ文字列で返す辞書。"""

    def __missing__(self, key: str) -> str:
        """存在しないキーを `{key}` 形式の文字列として返す。"""
        return f"{{{key}}}"
