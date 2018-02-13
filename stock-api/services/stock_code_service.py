from stores import StockCodeStore


class StockCodeService():
    store = StockCodeStore()

    def get(self):
        return self.store.get()