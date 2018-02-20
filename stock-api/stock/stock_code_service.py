from singleton import Singleton
from stores import StockCodeStore


class StockCodeService():
    __metaclass__ = Singleton

    store = StockCodeStore()

    def get(self):
        return self.store.get()