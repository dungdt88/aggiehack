import math
import heapq, random, sys
import constants
from datetime import datetime

def add_secs(dt, secs):
    if secs is not None:
        fulldate = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        fulldate = fulldate + datetime.timedelta(seconds = int(secs))
        return fulldate

def convert_sql_datetime_to_datetime(str_value):
    f = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(str_value, f)

from math import radians, cos, sin, asin, sqrt
def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def  get_xy_coord(lat, lon):
    x = distance(lat, lon, lat, constants.LONGTITUDE_LEFT_BOUND)
    y = distance(lat, lon, constants.LATITUDE_LOWER_BOUND, lon)
    return x, y

def get_moving_time(distance, velocity):
    return float(distance / velocity) * 3600

def from_datetime_to_str(datetime_value, format="%y-%m-%d-%H-%M-%S"):
    return datetime_value.strftime(format)

def from_str_to_datetime(str_value, format="%y-%m-%d-%H-%M-%S"):
    return datetime.datetime.strptime(str_value, format)

def get_difft_time(_end_time, _start_time):
    start_timetype = datetime.strptime(_start_time, "%y-%m-%d-%H-%M-%S")
    end_timetype   = datetime.strptime(_end_time, "%y-%m-%d-%H-%M-%S")
    return (end_timetype - start_timetype).seconds





