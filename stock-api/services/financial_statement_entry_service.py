from stores import FinancialStatementEntryStore


class FinancialStatementEntryService():
    store = FinancialStatementEntryStore()

    def get_roe(self, stock):
        store.get()
        return "FinancialStatementEntryService - ROE"
        #return self.store.get()

    def get_equity_multiplier(self, stock):
        return "FinancialStatementEntryService - Equity Multiplier"