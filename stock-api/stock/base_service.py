from singleton import Singleton
from stores import FinancialStatementEntryStore
from time_series import TimeSeries


class BaseService():
    __metaclass__ = Singleton

    store = FinancialStatementEntryStore()

    def build_data(self, stock_code, date_frame):
        raise NotImplementedError("Please Implement this method")

    def build_data_safely(self, stock_code, date_frame):
        try:
            return self.build_data(stock_code, date_frame)
        except:
            return []

    def get_metric(self, stock_code, date_frame, metric_name):
        metric = self.store.get(stock_code, metric_name)

        # Sanity check.
        if date_frame in metric:
            # Get yearly metric to annualize (if possible).
            if date_frame == u'Yearly' and u'Quarterly' in metric:
                return metric[date_frame].annualize(metric[u'Quarterly']).periodize()
            else:
                return metric[date_frame].periodize()
        else:
            return None

    def build_metric_data(self, metric, metric_name=None):
        try:
            return {
                'name': metric_name if metric_name is not None else metric.get()['name'],
                'date': metric.get()['date'],
                'value': metric.get()['value'],
            }
        except:
            return None

    def filter_list(self, item_list):
        return [entry for entry in item_list if entry is not None]

    def get_ratio(self, left_metric, right_metric, quarterly_scalar=1.0):
        result = left_metric / right_metric
        if result.date_frame == u'Quarterly':
            return result.scalar(quarterly_scalar)
        else:
            return result