from base_service import BaseService


class DividendPolicyService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Yearly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        # CashDividends = CashDividendsFromRetainedEarnings + CashDividendsFromCapitalReserve
        cash_dividends_from_retained_earnings = self.get_metric(stock_code, date_frame, 'CashDividendsFromRetainedEarnings')
        cash_dividends_from_capital_reserve = self.get_metric(stock_code, date_frame, 'CashDividendsFromCapitalReserve')
        cash_dividends = self.get_metric(stock_code, date_frame, 'CashDividends')

        # StockDividends = StockDividendsFromRetainedEarnings + StockDividendsFromCapitalReserve
        stock_dividends_from_retained_earnings = self.get_metric(stock_code, date_frame, 'StockDividendsFromRetainedEarnings')
        stock_dividends_from_capital_reserve = self.get_metric(stock_code, date_frame, 'StockDividendsFromCapitalReserve')
        stock_dividends = self.get_metric(stock_code, date_frame, 'StockDividends')

        employee_stock_bonus_ratio = self.get_metric(stock_code, date_frame, 'EmployeeStockBonusRatio')

        return [
            self.build_metric_data(cash_dividends_from_retained_earnings),
            self.build_metric_data(cash_dividends_from_capital_reserve),
            self.build_metric_data(cash_dividends),
            self.build_metric_data(stock_dividends_from_retained_earnings),
            self.build_metric_data(stock_dividends_from_capital_reserve),
            self.build_metric_data(stock_dividends),
            self.build_metric_data(employee_stock_bonus_ratio),
        ]