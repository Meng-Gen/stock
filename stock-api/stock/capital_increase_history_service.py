from base_service import BaseService


class CapitalIncreaseHistoryService(BaseService):
    def get(self, stock_code):
        metric_list = [
            self.get_metric(stock_code, 'CapitalIncreaseByCash'),
            self.get_metric(stock_code, 'CapitalIncreaseByEarnings'),
            self.get_metric(stock_code, 'CapitalIncreaseBySurplus'),
        ]
        grouped = self.group_by(metric_list)
        return [
            {
                'name': 'CapitalIncreaseHistoryService (Yearly)',
                'data': self._get_yearly_data(grouped),
            }
        ]

    def _get_yearly_data(self, grouped):
        if u'Yearly' in grouped:
            return [
                {
                    'name': 'CapitalIncreaseByCash',
                    'data': {
                        'date': grouped[u'Yearly']['CapitalIncreaseByCash'].get()['date'],
                        'value': grouped[u'Yearly']['CapitalIncreaseByCash'].get()['value'],
                    }
                },
                {
                    'name': 'CapitalIncreaseByEarnings',
                    'data': {
                        'date': grouped[u'Yearly']['CapitalIncreaseByEarnings'].get()['date'],
                        'value': grouped[u'Yearly']['CapitalIncreaseByEarnings'].get()['value'],
                    }
                },
                {
                    'name': 'CapitalIncreaseBySurplus',
                    'data': {
                        'date': grouped[u'Yearly']['CapitalIncreaseBySurplus'].get()['date'],
                        'value': grouped[u'Yearly']['CapitalIncreaseBySurplus'].get()['value'],
                    }
                },
            ]
        else:
            return []