from base_service import BaseService


class ExpectedRateOfReturnService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Yearly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Yearly')),
            },
            {
                'date_frame': u'Quarterly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Quarterly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        net_profit = self.get_metric(stock_code, date_frame, 'NetProfit')
        equity = self.get_metric(stock_code, date_frame, 'Equity')
        stock_price = self.get_metric(stock_code, date_frame, 'StockPrice')
        book_value = self.get_metric(stock_code, date_frame, 'BookValue')

        # ROE = (NetProfit / Sales) * (Sales / Assets) * (Assets / Equity)
        roe = self.get_ratio(net_profit, equity, 4.0)

        # max(PBR) = max(StockPrice) / BookValue
        max_pbr = self.get_ratio(stock_price.max(date_frame), book_value)

        # min(PBR) = min(StockPrice) / BookValue
        min_pbr = self.get_ratio(stock_price.min(date_frame), book_value)

        # max(ExpectedRateOfReturn) = ROE / min(PBR)
        max_expected_rate_of_return = self.get_ratio(roe, min_pbr)

        # min(ExpectedRateOfReturn) = ROE / max(PBR)        
        min_expected_rate_of_return = self.get_ratio(roe, max_pbr)

        return [
            self.build_metric_data(roe, 'ReturnOnEquity'),
            self.build_metric_data(max_pbr, 'MaxPbr'),
            self.build_metric_data(min_pbr, 'MinPbr'),
            self.build_metric_data(max_expected_rate_of_return, 'MaxExpectedRateOfReturn'),
            self.build_metric_data(min_expected_rate_of_return, 'MinExpectedRateOfReturn'),
        ]