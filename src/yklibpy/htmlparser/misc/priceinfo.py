class PriceInfo:
    def __init__(self, price_old, price_real):
        self.price_old = price_old
        self.price_real = price_real

    def get_price_old(self):
        if self.price_old is None:
            return None
        return self.price_old.get_option()

    def get_price_real(self):
        if self.price_real is None:
            return None
        return self.price_real.get_option()
