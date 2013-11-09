import math
import heapq, random, sys
import gmap_api
import datetime

def add_secs(dt, secs):
    if secs is not None:
        fulldate = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, 2)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
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
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def get_moving_time(distance, velocity):
    return float(distance / velocity) * 3600









