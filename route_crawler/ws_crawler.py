import requests
import datetime
import time 
from time import strptime, strftime
import sys
sys.path.insert(0, '../route_calculator/')
import db_util
from db_util import *
import cPickle
import os
import threading
from threading import *

DATA_DIR = "live_data"

class TransportationServiceAPI(): 
    def __init__(self):
        self.ts_api = 'http://transport.tamu.edu/BusRoutesFeed/api/buses/?route='
        
    def get_route_data(self, route_id):
        request = self.ts_api + route_id
        return requests.get(request).json()

def get_all_routes():
    sql_helper = SqlHelper()
    routes = sql_helper.get_all_route_names()
    return routes

def get_live_data(ts_api, route_names):

	now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

	for route_name in route_names:
		route_json = ts_api.get_route_data(route_name)
	
		if len(route_json) > 0:

			print route_name

			file_name = DATA_DIR + '/' + route_name + '-' + now + '.txt'
			f = open(file_name, 'wb')
			cPickle.dump(route_json, f)
			f.close()

if __name__ == '__main__':
	ts_api = TransportationServiceAPI()
	route_names = get_all_routes()

	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)

	t = Timer(10.0, get_live_data, args=(ts_api, route_names,))
	t.start()

	


