from calendar import monthrange
from datetime import datetime

import operator
import pandas as pd


class DatetimeUtils():
    @staticmethod
    def get_last_date_of_month_in_prev_year(timestamp):
        date = timestamp.to_pydatetime()
        year = date.year - 1
        month = date.month
        day = monthrange(year, month)[1]
        return datetime(year, month, day)


class TimeSeries(object):
    @staticmethod
    def create(name, date_frame, is_snapshot, dates, values):
        df = TimeSeries.__create_df(dates, values)
        return TimeSeries(name, date_frame, is_snapshot, df)

    @staticmethod
    def __create_df(dates, values):
        data = {
            'date': dates,
            'value': values,
        }
        df = pd.DataFrame(data, columns = ['date', 'value'])
        df.set_index(['date'], drop=True, inplace=True)
        df = df.sort_index()
        return df

    def __init__(self, name, date_frame, is_snapshot, df):
        self.name = name
        self.date_frame = date_frame
        self.is_snapshot = is_snapshot
        self.df = df.sort_index()

    def __repr__(self):
        return self.get().__repr__()

    def get(self):
        return {
            'name': self.name,
            'date_frame': self.date_frame,
            'is_snapshot': self.is_snapshot,
            'date': [index.to_pydatetime() for index, row in self.df.iterrows()],
            'value': [row['value'] for index, row in self.df.iterrows()],
        }

    def copy(self):
        return TimeSeries(self.name, self.date_frame, self.is_snapshot, self.df.copy())

    def shift(self):
        result = self.copy()
        result.df['value'] = result.df['value'].shift(1)
        result.df.fillna(method='bfill', inplace=True)
        return result

    def scalar(self, scale):
        result = self.copy()
        result.df['value'] = result.df['value'].apply(lambda x: scale * x)
        return result

    def inverse(self):
        result = self.copy()
        result.df['value'] = result.df['value'].apply(lambda x: 1.0 / x)
        return result

    def moving_average(self, n):
        result = self.copy()
        result.df['value'] = result.df.rolling(window=n, min_periods=1).mean()
        return result

    def accumulate(self):
        result = self.copy()
        result.df = result.df.cumsum()
        return result

    def accumulate_annually(self):
        result = self.copy()
        result.df = result.df.groupby(pd.Grouper(freq='A')).cumsum()
        return result

    def periodize(self):
        if self.is_snapshot:
            result = self.moving_average(2)
            result.is_snapshot = False
            return result
        else:
            return self

    def yoy(self):
        dates = []
        values = []
        for index, row in self.df.iterrows():
            prev_index = DatetimeUtils.get_last_date_of_month_in_prev_year(index)
            if prev_index not in self.df.index:
                continue
            dates.append(index.to_pydatetime())
            value = float(row['value'])
            prev_value = float(self.df.loc[prev_index, 'value'])
            values.append((value - prev_value) / prev_value)
        return TimeSeries.create(self.name, self.date_frame, self.is_snapshot, dates, values)

    def annualize(self, other):
        if self.date_frame != u'Yearly':
            raise ValueError(u'Cannot be annualized: {0}'.format(self.date_frame))
        if self.is_snapshot != other.is_snapshot:
            raise ValueError(u'The is_snapshot values are not matched.')

        if other.date_frame == u'Quarterly':
            this_year = self.df.index.max().year + 1
            this_date = datetime(year=this_year, month=12, day=31)
            this_value = other.df[str(this_year)].mean()[0]
            if not self.is_snapshot:
                this_value *= 4.0
            annualized_df = TimeSeries.__create_df([this_date], [this_value])
            result = pd.concat([self.df, annualized_df])
            result.sort_index()
            return TimeSeries(self.name, self.date_frame, self.is_snapshot, result)
        else:
            raise ValueError(u'Cannot annualize: {0}'.format(other.date_frame))

    def max(self, target_date_frame):
        result = self.copy()
        freq = self.__get_freq_for_pandas(target_date_frame)
        result.df = result.df.groupby(pd.Grouper(freq=freq)).max()
        result.date_frame = target_date_frame
        return result

    def min(self, target_date_frame):
        result = self.copy()
        freq = self.__get_freq_for_pandas(target_date_frame)
        result.df = result.df.groupby(pd.Grouper(freq=freq)).min()
        result.date_frame = target_date_frame
        return result

    def __get_freq_for_pandas(self, date_frame):
        if date_frame == u'Yearly':
            return 'A'
        elif date_frame == u'Quarterly':
            return 'Q'
        else:
            raise ValueError(u'Cannot get freq for pandas: {0}'.format(date_frame))

    def __execute_binary_operation(self, operator, other):
        if self.date_frame != other.date_frame:
            raise ValueError(u'The date_frame values are not matched.')
        if self.is_snapshot != other.is_snapshot:
            raise ValueError(u'The is_snapshot values are not matched.')

        left_operand = self.df.rename(columns={'value': 'left_value'})
        right_operand = other.df.rename(columns={'value': 'right_value'})

        result = left_operand.join(right_operand, how='outer')
        result.fillna(method='ffill', inplace=True)

        result['value'] = operator(result['left_value'], result['right_value'])

        del result['left_value']
        del result['right_value']

        result.dropna(inplace=True)

        return TimeSeries('', self.date_frame, self.is_snapshot, result)

    def __add__(self, other):
        return self.__execute_binary_operation(operator.add, other)

    def __sub__(self, other):
        return self.__execute_binary_operation(operator.sub, other)

    def __div__(self, other):
        return self.__execute_binary_operation(operator.truediv, other)

    def __mul__(self, other):
        return self.__execute_binary_operation(operator.mul, other)