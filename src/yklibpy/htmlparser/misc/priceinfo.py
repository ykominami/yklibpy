from yklibpy.htmlparser.misc.tagx import Tagx


class PriceInfo:
    """旧価格と現在価格の表示文字列をまとめて保持する。"""

    def __init__(self, price_old: Tagx | None, price_real: Tagx | None) -> None:
        """価格表示に対応する `Tagx` を保持する。"""
        self.price_old = price_old
        self.price_real = price_real

    def get_price_old(self) -> str | None:
        """保持している旧価格文字列を返す。"""
        if self.price_old is None:
            return None
        return self.price_old.get_option()

    def get_price_real(self) -> str | None:
        """保持している現在価格文字列を返す。"""
        if self.price_real is None:
            return None
        return self.price_real.get_option()
