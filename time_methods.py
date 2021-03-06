import datetime

def date_string(date_object):
    return date_object.__str__()

def date_object(date_string):
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    date = datetime.date(year, month, day)
    return date

def age_string(timedelta_object):
    return str(abs(int(timedelta_object.total_seconds() / 86400)))

def today():
    return date_string(datetime.date.today())

def now():
    now_string = date_string(datetime.datetime.now())
    now_string = now_string.replace('-','_')
    now_string = now_string.replace(' ','_')
    now_string = now_string.replace(':','_')
    return now_string[:-7]

def past_date(days):
    today = datetime.date.today()
    timedelta_object = datetime.timedelta(days = days, hours = 0, minutes = 0)
    past_date_object = today - timedelta_object
    past_date_string = date_string(past_date_object)
    return past_date_string

def future_date(date, days):
    timedelta_object = datetime.timedelta(days = days, hours = 0, minutes = 0)
    date_obj = date_object(date)
    future_date_object = date_obj + timedelta_object
    future_date_string = date_string(future_date_object)
    return future_date_string

def age(date_string_1, date_string_2):
    date_1 = date_object(date_string_1)
    date_2 = date_object(date_string_2)
    total_age = date_2 - date_1
    return age_string(total_age)

def past(date_string_1):
    date = date_object(date_string_1)
    if datetime.date.today() > date:
        return True
    return False
