import os
import json
import pprint
import util
from util import *

file_name = "live_data/bus.json"
sample_bus_id = "f532dcd5-4998-41b1-af0d-7b01e33da8f0"
sample_route_name = "12"

def get_bus_instance_data(bus_id, start_time_str, end_time_str):
  	bus_instance_data = [] # data [(time, dict of {key, lat, long, nextStop, estDepart}] for a particular bus ID

  	json_data = load_live_data_json_file()
  	# print json_data		
  	if json_data != None:

		for time_str, route_data in json_data.iteritems(): #key is datetime string, value is a dictionary of {route name, [bus instance data]}
			if time_str >= start_time_str and time_str <= end_time_str: #make sure it's in this time interval
				for route, bus_list in route_data.iteritems():
					for bus_data in bus_list:
						# print bus_data
						if bus_data['key'] == bus_id:
							bus_data['x'], bus_data['y'] = util.get_xy_coord(bus_data['lat'], bus_data['lng'])
							bus_instance_data.append((time_str, bus_data)) #tuple (time, bus_data)

		bus_instance_data = sorted(bus_instance_data, key=lambda item: item[0]) #sort list by time
		# pprint.pprint(bus_instance_data)
		print bus_instance_data
		print len(bus_instance_data)

	else:
		print 'Bus data not available.'

	return bus_instance_data

def get_random_bus_by_route(route_name):
	random_bus_id = None
  	json_data = load_live_data_json_file()	
  	if json_data != None:
  		route_data = json_data.items()[0][1]
  		if route_name in route_data:
  			bus_list_data = route_data[route_name]
  			bus_id_list = [i["key"] for i in bus_list_data]
  			
  			if len(bus_id_list) > 0:
				random_bus_id = bus_id_list[len(bus_id_list) - 1]

  	return random_bus_id

def load_live_data_json_file():
	if os.path.exists(file_name):
		with open(file_name) as f:
			json_data = json.load(f) # dict {datetime, dict {route name, [bus instance data]}}
			f.close()
			return json_data
	return None

if __name__ == '__main__':
	bus_id = get_random_bus_by_route(sample_route_name)
	if bus_id != None:
		get_bus_instance_data(bus_id, "13-11-22-12-45-00", "13-11-22-13-45-00")

