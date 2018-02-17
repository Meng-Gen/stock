from datetime import datetime
from items import FinancialStatementEntryDataItem
from items import FinancialStatementEntryItem

import operator
import pandas as pd


class TimeSeries(object):
    @staticmethod
    def create(date_frame, is_snapshot, dates, values):
        df = TimeSeries.create_df(dates, values)
        return TimeSeries(date_frame, is_snapshot, df)

    @staticmethod
    def create_df(dates, values):
        data = {
            'date': dates,
            'value': values,
        }
        df = pd.DataFrame(data, columns = ['date', 'value'])
        df.set_index(['date'], drop=True, inplace=True)
        df.sort_index()
        return df

    def __init__(self, date_frame, is_snapshot, df):
        self.date_frame = date_frame
        self.is_snapshot = is_snapshot
        self.df = df.sort_index()

    def __repr__(self):
        return 'date_frame: {date_frame}\nis_snapshot: {is_snapshot}\ndf: \n{df}' \
            .format(date_frame=self.date_frame, is_snapshot=self.is_snapshot, df=self.df)

    def copy(self):
        return TimeSeries(self.date_frame, self.is_snapshot, self.df.copy())

    def shift(self):
        result = self.copy()
        result.df['value'] = result.df['value'].shift(1)
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
        for index, row in self.df.iterrows():
            print type(index), row
            print index.replace(year=index.year - 1)



        #result = self.copy()
        #print result.df

    def execute_binary_operation(self, operator, other):
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

        return TimeSeries(self.date_frame, self.is_snapshot, result)

    def __add__(self, other):
        return self.execute_binary_operation(operator.add, other)

    def __sub__(self, other):
        return self.execute_binary_operation(operator.sub, other)

    def __div__(self, other):
        return self.execute_binary_operation(operator.truediv, other)

    def __mul__(self, other):
        return self.execute_binary_operation(operator.mul, other)


def main():
    dates = [
        datetime(2016, 12, 31, 0, 0), 
        datetime(2016, 9, 30, 0, 0), 
        datetime(2016, 6, 30, 0, 0), 
        datetime(2016, 3, 31, 0, 0), 
        datetime(2015, 12, 31, 0, 0), 
        datetime(2015, 9, 30, 0, 0), 
        datetime(2015, 6, 30, 0, 0), 
        datetime(2015, 3, 31, 0, 0), 
    ]
    values = [10, 20, 30, 40, 50, 60, 70, 80]
    ts1 = TimeSeries.create(
        date_frame=u'Yearly',
        is_snapshot=True,
        dates=dates,
        values=values
    )

    #print ts1
    #print ts1.scalar(365.0)
    #print ts1.shift()
    #print ts1.moving_average(2)
    #print ts1.periodize()
    print ts1.yoy()

if __name__ == '__main__':
    main()
