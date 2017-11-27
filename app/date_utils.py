from pytz import timezone
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)


def local_to_utc(date, tz_name):
    return date - get_timezone_offset(date, tz_name)


def utc_to_local(date, tz_name):
    return date + get_timezone_offset(date, tz_name)


def get_timezone_offset(date, tz_name):
    return timezone(tz_name).localize(date).utcoffset()


def get_yesterday_dt():
    yesterday = date.today() - timedelta(1)
    # Add time to date object
    return datetime.combine(yesterday, time.min)
