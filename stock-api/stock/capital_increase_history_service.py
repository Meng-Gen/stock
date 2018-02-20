from base_service import BaseService


class CapitalIncreaseHistoryService(BaseService):
    def get(self, stock_code):
        metric_list = [
            self.get_metric(stock_code, 'CapitalIncreaseByCash'),
            self.get_metric(stock_code, 'CapitalIncreaseByEarnings'),
            self.get_metric(stock_code, 'CapitalIncreaseBySurplus'),
        ]

        grouped = self.group_by(metric_list)
        if u'Yearly' not in grouped:
            raise ValueError(u'Capital increase history should be yearly')

        print grouped[u'Yearly']
