from base_service import BaseService


class CapitalIncreaseHistoryService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Yearly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        capital_increase_by_cash = self.get_metric(stock_code, date_frame, 'CapitalIncreaseByCash')
        capital_increase_by_earnings = self.get_metric(stock_code, date_frame, 'CapitalIncreaseByEarnings')
        capital_increase_by_surplus = self.get_metric(stock_code, date_frame, 'CapitalIncreaseBySurplus')

        return [
            self.build_metric_data(capital_increase_by_cash),
            self.build_metric_data(capital_increase_by_earnings),
            self.build_metric_data(capital_increase_by_surplus),
        ]