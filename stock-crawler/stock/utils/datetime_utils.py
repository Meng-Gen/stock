from calendar import monthrange
from datetime import datetime
from dateutil.rrule import MONTHLY
from dateutil.rrule import YEARLY
from dateutil.rrule import rrule


def build_datetime_from_year(data):
    year = int(data)
    return datetime(year=year, month=12, day=31)

def build_datetime_from_roc_era(data):
    year = int(data) + 1911
    return datetime(year=year, month=12, day=31)

def build_datetime_from_roc_era_with_quarter(data):
    roc_era_and_quarter = data.split('.')
    if len(roc_era_and_quarter) != 2:
        raise ValueError(u'Could not parse ROC era and quarter: {0}'.format(data))

    roc_era, quarter = roc_era_and_quarter
    year = int(roc_era) + 1911
    if quarter == '1Q':
        return datetime(year=year, month=3, day=31)
    elif quarter == '2Q':
        return datetime(year=year, month=6, day=30)
    elif quarter == '3Q':
        return datetime(year=year, month=9, day=30)
    elif quarter == '4Q':
        return datetime(year=year, month=12, day=31)
    else:
        raise ValueError(u'Could not parse ROC era and quarter: {0}'.format(data))

def build_datetime_from_roc_era_and_month(roc_era, month):
    year = int(roc_era) + 1911
    month = int(month)
    day = monthrange(year, month)[1]
    return datetime(year=year, month=month, day=day)

def build_datetime_from_roc_era_with_month(data):
    roc_era_and_month = data.split('/')
    if len(roc_era_and_month) != 2:
        raise ValueError(u'Could not parse ROC era and month: {0}'.format(data))

    roc_era, month = roc_era_and_month
    year = int(roc_era) + 1911
    month = int(month)
    day = monthrange(year, month)[1]
    return datetime(year=year, month=month, day=day)

def build_datetime_from_roc_era_with_month_and_day(data):
    roc_era_and_month_and_day = data.split('/')
    if len(roc_era_and_month_and_day) != 3:
        raise ValueError(u'Could not parse ROC era and month and day: {0}'.format(data))

    roc_era, month, day = roc_era_and_month_and_day
    year = int(roc_era) + 1911
    month = int(month)
    day = int(day)
    return datetime(year=year, month=month, day=day)

def month_range(start_date, end_date):
    return list(rrule(freq=MONTHLY, dtstart=start_date.replace(day=1), until=end_date))[::-1]

def year_range(start_date, end_date):
    return list(rrule(freq=YEARLY, dtstart=start_date.replace(day=1).replace(month=1), until=end_date))[::-1]