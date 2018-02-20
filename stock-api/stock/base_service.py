from singleton import Singleton
from stores import FinancialStatementEntryStore


class BaseService():
    __metaclass__ = Singleton

    store = FinancialStatementEntryStore()
    date_frames = [u'Yearly', u'Quarterly', u'Monthly', u'Biweekly', u'Weekly', u'Daily']

    def get_metric(self, stock_code, metric_name):
        return self.store.get(stock_code, metric_name)

    def group_by(self, metric_list):
        """Group metric list by date frame.

        Args:
            metric_list: A list of metric map. A metric map is a map mapping
            date_frame strings to TimeSeries objects. For example:
            [
                {
                    u'Yearly': TimeSeries(),
                    u'Quarterly': TimeSeries(),
                },
                {
                    u'Yearly': TimeSeries(),
                    u'Quarterly': TimeSeries(),
                },
                {
                    u'Yearly': TimeSeries(),
                    u'Quarterly': TimeSeries(),
                },
            ]

        Returns:
            A map which keys are date_frame strings and values are maps mapping
            metric names to TimeSeries objects. For example:
            {
                u'Yearly': {
                    u'Assets': TimeSeries(),
                    u'Liabilities': TimeSeries(),
                    u'Equity': TimeSeries(),
                },
                u'Quarterly':{
                    u'Assets': TimeSeries(),
                    u'Liabilities': TimeSeries(),
                    u'Equity': TimeSeries(),
                },
            }
        """
        grouped = {}
        for date_frame in self.date_frames:
            for metric in metric_list:
                if date_frame in metric:
                    if date_frame not in grouped:
                        grouped[date_frame] = {}
                    time_series = metric[date_frame]
                    grouped[date_frame][time_series.name] = time_series
        return grouped