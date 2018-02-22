from singleton import Singleton
from stores import FinancialStatementEntryStore


class BaseService():
    __metaclass__ = Singleton

    store = FinancialStatementEntryStore()

    def get_metric(self, stock_code, date_frame, metric_name):
        metric = self.store.get(stock_code, metric_name)

        # Get yearly metric
        if date_frame == u'Yearly':
            if u'Yearly' in metric:
                if u'Quarterly' in metric:
                    return metric[u'Yearly'].annualize(metric[u'Quarterly']).periodize()
                else:
                    return metric[u'Yearly'].periodize()
            else:
                return None
        # Get quarterly metric
        elif date_frame == u'Quarterly':
            if u'Quarterly' in metric:
                return metric[u'Quarterly'].periodize()
            else:
                return None
        else:
            return None

    def build_metric_data(self, metric, metric_name):
        try:
            return {
                'name': metric_name,
                'date': metric.get()['date'],
                'value': metric.get()['value'],
            }
        except:
            return None

    def filter_list(self, item_list):
        return [entry for entry in item_list if entry is not None]

    def get_ratio(self, left_operand, right_operand, quarterly_scalar=1.0):
        result = left_operand / right_operand
        if result.date_frame == u'Quarterly':
            return result.scalar(quarterly_scalar)
        else:
            return result