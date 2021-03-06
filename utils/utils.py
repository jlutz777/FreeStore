import pytz, datetime
from fuzzywuzzy import fuzz

datetime_fmt = "%m/%d/%Y %H:%M"
date_fmt = "%m/%d/%Y"
utc_tz = pytz.utc
local_tz = pytz.timezone('US/Eastern')


def formatted_str_date(my_date):
    if my_date is None:
        return None

    str_date = my_date.strftime(date_fmt)
    return str_date

def formatted_str_date_time(my_date):
    if my_date is None:
        return None

    str_date = my_date.strftime(datetime_fmt)
    return str_date

def local_time_to_utc_time(local_time):
    if local_time is None:
        return None

    dt = local_time
    if isinstance(dt, str):
        dt = datetime.datetime.strptime(dt, datetime_fmt)
    local_dt = local_tz.localize(dt)
    return local_dt.astimezone(utc_tz).strftime(datetime_fmt)

def utc_time_to_local_time(utc_time):
    if utc_time is None:
        return None

    dt = utc_time
    if isinstance(dt, str):
        dt = datetime.datetime.strptime(dt, datetime_fmt)
    utc_dt = utc_tz.localize(dt)
    return utc_dt.astimezone(local_tz).strftime(datetime_fmt)

def is_fuzzy_match(data1, data2, accuracy=80):
    matchVal = fuzz.ratio(data1, data2)
    return matchVal > accuracy
