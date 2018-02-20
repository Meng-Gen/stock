from time_series import TimeSeries


class MockFinancialStatementEntryStore(object):
    def get(self, stock_code, metric_name):
        return {
            u'Yearly': TimeSeries.create(
                date_frame=u'Yearly',
                is_snapshot=False,
                dates=[],
                values=[]
            ),
            u'Quarterly': TimeSeries.create(
                date_frame=u'Quarterly',
                is_snapshot=False,
                dates=[],
                values=[]
            ),
        }