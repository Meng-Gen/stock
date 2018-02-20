from datetime import datetime

from time_series import TimeSeries


class MockMetricNames(object):
    def get(self, good_metric_name):
        return good_metric_name


class MockFinancialStatementEntryStore(object):
    mock_data = {
        '2317': {
            'CapitalIncreaseByCash': {
                u'Yearly': TimeSeries.create(
                    name=u'CapitalIncreaseByCash',
                    date_frame=u'Yearly',
                    is_snapshot=False,
                    dates=[datetime(2005, 12, 31), datetime(2006, 12, 31), datetime(2007, 12, 31)],
                    values=[26.44, 27.01, 27.01]
                ),
            },
            'CapitalIncreaseByEarnings': {
                u'Yearly': TimeSeries.create(
                    name=u'CapitalIncreaseByEarnings',
                    date_frame=u'Yearly',
                    is_snapshot=False,
                    dates=[datetime(2005, 12, 31), datetime(2006, 12, 31), datetime(2007, 12, 31)],
                    values=[346.52, 435.51, 547.78]
                ),
            },
            'CapitalIncreaseBySurplus': {
                u'Yearly': TimeSeries.create(
                    name=u'CapitalIncreaseBySurplus',
                    date_frame=u'Yearly',
                    is_snapshot=False,
                    dates=[datetime(2005, 12, 31), datetime(2006, 12, 31), datetime(2007, 12, 31)],
                    values=[36.01, 53.83, 53.83]
                ),
            },
        }
    }

    def get(self, stock_code, metric_name):
        if stock_code in self.mock_data:
            if metric_name in self.mock_data[stock_code]:
                return self.mock_data[stock_code][metric_name]

        return {
            u'Yearly': TimeSeries.create(
                name=u'Mock',
                date_frame=u'Yearly',
                is_snapshot=False,
                dates=[],
                values=[]
            ),
            u'Quarterly': TimeSeries.create(
                name=u'Mock',
                date_frame=u'Quarterly',
                is_snapshot=False,
                dates=[],
                values=[]
            ),
        }