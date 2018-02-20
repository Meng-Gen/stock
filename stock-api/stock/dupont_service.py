from metric_names import MetricNames
from singleton import Singleton
from stores import FinancialStatementEntryStore
from time_series import TimeSeries


class DupontService():
    __metaclass__ = Singleton

    store = FinancialStatementEntryStore()
    metric_names = MetricNames()

    def roe(self, stock_code):
        net_profit_list = self.store.get(stock_code, self.metric_names.get('NetProfit'))
        print net_profit_list
        # Yearly and Quarterly

        return "FinancialStatementEntryService - ROE"

    def equity_multiplier(self, stock_code):
        return "FinancialStatementEntryService - Equity Multiplier"