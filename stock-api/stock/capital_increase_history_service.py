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

        return [
            {
                'name': 'CapitalIncreaseHistoryService (Yearly)',
                'data': [
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
            }
        ]