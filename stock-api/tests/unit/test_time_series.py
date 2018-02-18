from datetime import datetime
from time_series import TimeSeries

import unittest


class TimeSeriesTest(unittest.TestCase):
    def test_create(self):
        ts = TimeSeries.create(
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 6, 30, 0, 0), datetime(2016, 3, 31, 0, 0)],
            values=[100, 200]
        )
        expected = {
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31, 0, 0), datetime(2016, 6, 30, 0, 0)],
            'value': [200, 100],
        }
        self.assertEqual(ts.get(), expected)

    def test_copy(self):
        original = TimeSeries.create(
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 6, 30, 0, 0), datetime(2016, 3, 31, 0, 0)],
            values=[100, 200]
        )
        original_expected = {
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31, 0, 0), datetime(2016, 6, 30, 0, 0)],
            'value': [200, 100],
        }

        # Make a copy.
        copied = original.copy()

        # Original time series won't be changed even we modify copied one.
        copied.date_frame = u'Yearly'
        copied.is_snapshot = True
        copied.df = TimeSeries.create_df([datetime(2016, 9, 30, 0, 0)], [300])
        copied_expected = {
            'date_frame': u'Yearly',
            'is_snapshot': True,
            'date': [datetime(2016, 9, 30, 0, 0)],
            'value': [300],
        }

        self.assertEqual(original.get(), original_expected)
        self.assertEqual(copied.get(), copied_expected)


    """
    dates = [
        datetime(2016, 9, 30, 0, 0), 
        datetime(2016, 6, 30, 0, 0), 
        datetime(2016, 3, 31, 0, 0), 
        datetime(2015, 12, 31, 0, 0), 
        datetime(2015, 9, 30, 0, 0), 
        datetime(2015, 6, 30, 0, 0), 
        datetime(2015, 3, 31, 0, 0), 
    ]
    values = [10, 20, 30, 40, 50, 60, 70]
    ts1 = TimeSeries.create(
        date_frame=u'Quarterly',
        is_snapshot=False,
        dates=dates,
        values=values
    )

    ts2 = TimeSeries.create(
        date_frame=u'Yearly',
        is_snapshot=False,
        dates=[datetime(2015, 12, 31, 0, 0)],
        values=[10]
    )
    
    print ts2
    #print ts2.annualize(ts1)

    #print ts1 / ts1.scalar(3)
    #print ts1.scalar(365.0)
    #print ts1.shift()
    #print ts1.moving_average(2)
    #print ts1.periodize()
    #print ts1.yoy()
    print ts1.get()
    """