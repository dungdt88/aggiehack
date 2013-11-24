import os
import json
import pprint
import util
from util import *
import datetime

file_name = "live_data/bus.json"
sample_bus_id = "cb227902-a30c-4c00-b9c1-c3af9321769d" #bus id of route 15 on Sat 11/23/13    #"699ed7ed-31f0-4a98-853b-50a43593d647" #bus id of route 12 on Sate 11/23/13
sample_start_time_str = "13-11-23-13-30-00"
sample_end_time_str = "13-11-23-14-35-00"

def print_bus_data(bus_instance_data):
	for i in bus_instance_data:
		print i

def get_bus_instance_data(bus_id, start_time_str, end_time_str):
  	bus_instance_data = [] # data [(time, dict of {key, lat, long, nextStop, estDepart}] for a particular bus ID

  	json_data = load_live_data_json_file()
  	# print json_data		
  	if json_data != None:

		for time_str, route_data in json_data: #key is datetime string, value is a dictionary of {route name, [bus instance data]}
			if time_str >= start_time_str and time_str <= end_time_str: #make sure it's in this time interval
				for route, bus_list in route_data.iteritems():
					for bus_data in bus_list:
						# print bus_data
						if bus_data['key'] == bus_id:
							x, y = util.get_xy_coord(bus_data['lat'], bus_data['lng'])
							bus_instance_data.append((str(time_str), x, y, float(bus_data['lat']), float(bus_data['lng']), int(bus_data['direction']), str(bus_data['occupancy']), str(bus_data['nextStop']), str(bus_data['estDepart']))) #tuple (time, bus_data)

		bus_instance_data = sorted(bus_instance_data, key=lambda item: item[0]) #sort list by time

		print_bus_data(bus_instance_data)

	else:
		print 'Bus data not available.'

	return bus_instance_data


def load_live_data_json_file():
	if os.path.exists(file_name):
		with open(file_name) as f:
			json_data = json.load(f) # [(datetime, dict {route name, [bus instance data]}]
			f.close()
			return json_data
	return None

if __name__ == '__main__':
	get_bus_instance_data(sample_bus_id, sample_start_time_str, sample_end_time_str)

