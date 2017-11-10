import time
import datetime

import dateutil.parser

def time_now_str(offset_weeks=0):
    date = datetime.datetime.utcnow()
    date = date + datetime.timedelta(weeks=offset_weeks)
    return date.isoformat() + 'Z' # 'Z' indicates UTC time

def convert_datetime(utc_str):
    return dateutil.parser.parse(utc_str)
