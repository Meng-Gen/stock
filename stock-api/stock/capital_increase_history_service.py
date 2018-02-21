from base_service import BaseService


class CapitalIncreaseHistoryService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data(stock_code, u'Yearly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        metric_names = [
            'CapitalIncreaseByCash',
            'CapitalIncreaseByEarnings',
            'CapitalIncreaseBySurplus',
        ]
        return [
            self.build_metric_data(self.get_metric(stock_code, date_frame, metric_name), metric_name) \
                for metric_name in metric_names
        ]