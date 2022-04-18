from pytz import timezone
from datetime import (
    date,
    timedelta,
)

from app import nyc_holidays


def local_to_utc(date, tz_name):
    return date - get_timezone_offset(date, tz_name)


def utc_to_local(date, tz_name):
    return date + get_timezone_offset(date, tz_name)


def get_timezone_offset(date, tz_name):
    return timezone(tz_name).localize(date).utcoffset()


def calculate_date_received():
    date_received = date.today()
    while date_received.isoweekday() in {6, 7} or date_received in nyc_holidays:
        date_received += timedelta(days=1)
    return date_received
