from base_service import BaseService


class DupontService(BaseService):
    def get(self, stock_code):
        return {
            'DuPont': [
                {
                    'date_frame': u'Yearly',
                    'data': self.filter_list(self.build_data(stock_code, u'Yearly')),
                },
                {
                    'date_frame': u'Quarterly',
                    'data': self.filter_list(self.build_data(stock_code, u'Quarterly')),
                },
            ]
        }

    def build_data(self, stock_code, date_frame):
        net_profit = self.get_metric(stock_code, date_frame, 'NetProfit')
        equity = self.get_metric(stock_code, date_frame, 'Equity')
        assets = self.get_metric(stock_code, date_frame, 'Assets')
        sales = self.get_metric(stock_code, date_frame, 'Sales')

        roe = self.get_ratio(net_profit, equity, 4.0)
        roa = self.get_ratio(net_profit, assets, 4.0)

        # ROE = (NetProfit / Sales) * (Sales / Assets) * (Assets / Equity)
        ros = self.get_ratio(net_profit, sales, 4.0)
        ato = self.get_ratio(sales, assets, 4.0)
        equity_multiplier = self.get_ratio(assets, equity, 1.0)

        return [
            self.build_metric_data(roe, 'ReturnOnEquity'),
            self.build_metric_data(roa, 'ReturnOnAssets'),
            self.build_metric_data(ros, 'ReturnOnSales'),
            self.build_metric_data(ato, 'AssetTurnover'),
            self.build_metric_data(equity_multiplier, 'EquityMultiplier'),
        ]

    def get_ratio(self, left_operand, right_operand, quarterly_scalar=1.0):
        result = left_operand / right_operand
        if result.date_frame == u'Quarterly':
            return result.scalar(quarterly_scalar)
        else:
            return result