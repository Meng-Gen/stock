from stores import DateFrame
from stores import StockCodeStore


class StockCodeService():
    store = StockCodeStore()

    def get(self):
        return self.store.get()


class DupontService():
    pass