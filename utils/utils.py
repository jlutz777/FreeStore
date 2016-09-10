import pytz

def date_in_time_zone(my_date):
    utc_date = my_date.replace(tzinfo=pytz.utc)
    time_zone_aware_date = utc_date.astimezone(pytz.timezone('America/Detroit'))
    formatted_nicely = time_zone_aware_date.strftime("%m/%d/%Y %H:%M")
    return formatted_nicely

def formatted_str_date(my_date):
    str_date = my_date.strftime("%m/%d/%Y %H:%M")
    return str_date
