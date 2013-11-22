import requests
import datetime
import time 
from time import strptime, strftime
import sys
sys.path.insert(0, '../route_calculator/')
import db_util
from db_util import *
import json
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
	#start another thread to get data
	t = Timer(10.0, get_live_data, args=(ts_api, route_names,))
	t.start()

	#get data
	now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
	data = {}

	file_name = DATA_DIR + '/bus.json'

	if os.path.exists(file_name):
		with open(file_name) as f:
			data = json.load(f) # dict {datetime, dict {route name, [bus instance data]}}
			f.close()

	route_dict = {}
	for route_name in route_names:

		route_json = ts_api.get_route_data(route_name)
	
		if len(route_json) > 0:
			route_dict[route_name] = route_json

	data[now] = route_dict	
		
	with open(file_name, 'w') as f:	
		f.write(json.dumps(data))
		f.close()

	str_result = "Successfully updated %s; Number of routes: %s" %(now, len(route_dict))
	with open(DATA_DIR + '/log.txt', 'a') as log_file:
		log_file.write(str_result + '\n')
	print str_result


if __name__ == '__main__':
	ts_api = TransportationServiceAPI()
	route_names = get_all_routes()

	if not os.path.exists(DATA_DIR):
		os.makedirs(DATA_DIR)

	get_live_data(ts_api, route_names)

	# while True:
	# 	get_live_data(ts_api, route_names)
	# 	time.sleep(10)


	


