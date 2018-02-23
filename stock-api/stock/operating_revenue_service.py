from base_service import BaseService


class OperatingRevenueService(BaseService):
    def get(self, stock_code):
        return [
            {
                'date_frame': u'Monthly',
                'data': self.filter_list(self.build_data_safely(stock_code, u'Monthly')),
            },
        ]

    def build_data(self, stock_code, date_frame):
        operating_revenue = self.get_metric(stock_code, date_frame, 'OperatingRevenue')
        accumulated_operating_revenue = operating_revenue.accumulate_annually()
        accumulated_operating_revenue_yoy = accumulated_operating_revenue.yoy()
        long_term_average = operating_revenue.moving_average(12)
        short_term_average = operating_revenue.moving_average(3)

        return [
            self.build_metric_data(operating_revenue),
            self.build_metric_data(accumulated_operating_revenue, 'AccumulatedOperatingRevenue'),
            self.build_metric_data(accumulated_operating_revenue_yoy, 'AccumulatedOperatingRevenueYoy'),
            self.build_metric_data(long_term_average, 'LongTermAverage'),
            self.build_metric_data(short_term_average, 'ShortTermAverage'),
        ]