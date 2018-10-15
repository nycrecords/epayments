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
