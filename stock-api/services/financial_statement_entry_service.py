from services.metric_names import MetricNames
from stores import FinancialStatementEntryStore
from time_series import TimeSeries


class FinancialStatementEntryService():
    store = FinancialStatementEntryStore()
    metric_names = MetricNames()

    def get_roe(self, stock):
        time_series_list = self.store.get(self.metric_names.get('NetProfit'))
        print time_series_list
        # Yearly and Quarterly
        
        return "FinancialStatementEntryService - ROE"

    def get_equity_multiplier(self, stock):
        return "FinancialStatementEntryService - Equity Multiplier"