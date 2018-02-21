from base_service import BaseService


class DupontService(BaseService):
    def get(self, stock_code):
        return {
            'DuPont': [
                {
                    'date_frame': u'Yearly',
                    'data': self.filter_list(self.build_data(stock_code, u'Yearly')),
                },
            ]
        }

    def build_data(self, stock_code, date_frame):
        #net_profit = self.get_metric(stock_code, date_frame, 'NetProfit')
        #equity = self.get_metric(stock_code, date_frame, 'Equity')
        #assets = self.get_metric(stock_code, date_frame, 'Assets')
        #sales = self.get_metric(stock_code, date_frame, 'Sales')
        #roe = net_profit / equity


        return [
        ]