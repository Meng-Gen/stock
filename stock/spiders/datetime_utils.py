from datetime import datetime


def build_datetime_from_roc_era(roc_era):
    year = int(roc_era) + 1911
    return datetime(year=year, month=12, day=31)