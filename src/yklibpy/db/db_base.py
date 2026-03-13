class DbBase:
    """辞書ベースのストレージ実装が共有する基底クラス。"""

    def __init__(self) -> None:
        """空の連想配列を内部状態として初期化する。"""
        self.assoc: dict[str, object] = {}
