from stores import FinancialStatementEntryStore


class FinancialStatementEntryService():
    store = FinancialStatementEntryStore()

    def get_roe(self, stock):
        self.store.get(u'\u7d93\u5e38\u5229\u76ca')
        return "FinancialStatementEntryService - ROE"
        #return self.store.get()

    def get_equity_multiplier(self, stock):
        return "FinancialStatementEntryService - Equity Multiplier"