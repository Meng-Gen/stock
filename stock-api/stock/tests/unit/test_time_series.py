from datetime import datetime
from time_series import TimeSeries

import unittest


class TimeSeriesTest(unittest.TestCase):
    def test_create(self):
        ts = TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 6, 30), datetime(2016, 3, 31)],
            values=[100, 200]
        )

        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30)],
            'value': [200, 100],
        }
        self.assertEqual(ts.get(), expected)

    def test_copy(self):
        original = TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 3, 31), datetime(2016, 6, 30)],
            values=[100.0, 200.0]
        )

        original_expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30)],
            'value': [100.0, 200.0],
        }

        # Make a copy.
        copied = original.copy()

        # Original time series won't be changed even we modify copied one.
        copied.name = u'Copied'
        copied.date_frame = u'Yearly'
        copied.is_snapshot = True
        copied_expected = {
            'name': u'Copied',
            'date_frame': u'Yearly',
            'is_snapshot': True,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30)],
            'value': [100.0, 200.0],
        }

        self.assertEqual(original.get(), original_expected)
        self.assertEqual(copied.get(), copied_expected)

    def test_shift(self):
        ts = self._create_test_ts()
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0, 100.0, 200.0],
        }
        self.assertEqual(ts.shift().get(), expected)

    def test_scalar(self):
        ts = self._create_test_ts()
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [300.0, 600.0, 900.0],
        }
        self.assertEqual(ts.scalar(3).get(), expected)

    def test_inverse(self):
        ts = self._create_test_ts()
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [1.0 / 100.0, 1.0 / 200.0, 1.0 / 300.0],
        }
        self.assertEqual(ts.inverse().get(), expected)

    def test_moving_average(self):
        ts = self._create_test_ts()
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0, (100.0 + 200.0) / 2.0, (200.0 + 300.0) / 2.0],
        }
        self.assertEqual(ts.moving_average(2).get(), expected)

    def test_accumulate(self):
        ts = self._create_test_ts()
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0, 100.0 + 200.0, 100.0 + 200.0 + 300.0],
        }
        self.assertEqual(ts.accumulate().get(), expected)

    def test_accumulate_annually(self):
        ts = TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[
                datetime(2015, 3, 31), datetime(2015, 6, 30), datetime(2015, 9, 30), datetime(2015, 12, 31),
                datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30), datetime(2016, 12, 31)
            ],
            values=[
                100.0, 200.0, 300.0, 400.0,
                500.0, 600.0, 700.0, 800.0
            ]
        )
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [
                datetime(2015, 3, 31), datetime(2015, 6, 30), datetime(2015, 9, 30), datetime(2015, 12, 31),
                datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30), datetime(2016, 12, 31)
            ],
            'value': [
                100.0, 100.0 + 200.0, 100.0 + 200.0 + 300.0, 100.0 + 200.0 + 300.0 + 400.0,
                500.0, 500.0 + 600.0, 500.0 + 600.0 + 700.0, 500.0 + 600.0 + 700.0 + 800.0
            ],
        }
        self.assertEqual(ts.accumulate_annually().get(), expected)

    def test_periodize_snapshot(self):
        ts = self._create_test_ts()
        ts.is_snapshot = True
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0, 150.0, 250.0],
        }
        self.assertEqual(ts.periodize().get(), expected)

    def test_periodize_nonsnapshot(self):
        ts = self._create_test_ts()
        # Leave unchanged if non-snapshot.
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0, 200.0, 300.0],
        }
        self.assertEqual(ts.periodize().get(), expected)

    def test_yoy(self):
        ts = TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[
                datetime(2015, 3, 31), datetime(2015, 6, 30), datetime(2015, 9, 30), datetime(2015, 12, 31),
                datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30), datetime(2016, 12, 31)
            ],
            values=[
                100.0, 200.0, 300.0, 400.0,
                500.0, 600.0, 700.0, 800.0
            ]
        )
        expected = {
            'name': u'Test',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [
                datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30), datetime(2016, 12, 31)
            ],
            'value': [
                (500.0 - 100.0) / 100.0,
                (600.0 - 200.0) / 200.0,
                (700.0 - 300.0) / 300.0,
                (800.0 - 400.0) / 400.0,
            ],
        }
        self.assertEqual(ts.yoy().get(), expected)

    def test_annualize(self):
        one = TimeSeries.create(
            name=u'Test',
            date_frame=u'Yearly',
            is_snapshot=False,
            dates=[datetime(2013, 12, 31), datetime(2014, 12, 31), datetime(2015, 12, 31)],
            values=[100.0, 200.0, 300.0]
        )
        other = TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            values=[400.0, 500.0, 600.0]
        )
        expected = {
            'name': u'Test',
            'date_frame': u'Yearly',
            'is_snapshot': False,
            'date': [datetime(2013, 12, 31), datetime(2014, 12, 31), datetime(2015, 12, 31), datetime(2016, 12, 31)],
            'value': [100.0, 200.0, 300.0, 2000.0],
        }
        self.assertEqual(one.annualize(other).get(), expected)

    def test_add(self):
        one = self._create_one_ts()
        other = self._create_other_ts()
        expected = {
            'name': u'One',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0 + 400.0, 200.0 + 500.0, 300.0 + 600.0],
        }
        self.assertEqual((one + other).get(), expected)

    def test_sub(self):
        one = self._create_one_ts()
        other = self._create_other_ts()
        expected = {
            'name': u'One',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0 - 400.0, 200.0 - 500.0, 300.0 - 600.0],
        }
        self.assertEqual((one - other).get(), expected)

    def test_div(self):
        one = self._create_one_ts()
        other = self._create_other_ts()
        expected = {
            'name': u'One',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0 / 400.0, 200.0 / 500.0, 300.0 / 600.0],
        }
        self.assertEqual((one / other).get(), expected)

    def test_mul(self):
        one = self._create_one_ts()
        other = self._create_other_ts()
        expected = {
            'name': u'One',
            'date_frame': u'Quarterly',
            'is_snapshot': False,
            'date': [datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            'value': [100.0 * 400.0, 200.0 * 500.0, 300.0 * 600.0],
        }
        self.assertEqual((one * other).get(), expected)

    def _create_test_ts(self):
        return TimeSeries.create(
            name=u'Test',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            values=[100.0, 200.0, 300.0]
        )

    def _create_one_ts(self):
        return TimeSeries.create(
            name=u'One',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            values=[100.0, 200.0, 300.0]
        )

    def _create_other_ts(self):
        return TimeSeries.create(
            name=u'Other',
            date_frame=u'Quarterly',
            is_snapshot=False,
            dates=[datetime(2016, 3, 31), datetime(2016, 6, 30), datetime(2016, 9, 30)],
            values=[400.0, 500.0, 600.0]
        )