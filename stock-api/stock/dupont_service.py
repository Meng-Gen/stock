from base_service import BaseService


class DupontService(BaseService):
    def roe(self, stock_code):
        net_profit = self.get_metric(stock_code, 'NetProfit')
        print net_profit
        # Yearly and Quarterly

        return "FinancialStatementEntryService - ROE"

    def equity_multiplier(self, stock_code):
        return "FinancialStatementEntryService - Equity Multiplier"