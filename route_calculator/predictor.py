import sys
sys.path.insert(0, '../route_crawler/')
import os
import json
import pprint

file_name = "../route_crawler/live_data/bus.json"

def get_bus_instance_data(bus_id, start_time_str, end_time_str):
  	bus_instance_data = [] # data [(time, dict of {key, lat, long, nextStop, estDepart}] for a particular bus ID


  	json_data = load_json_file()
  	# print json_data		
  	if json_data != None:

		for time_str, route_data in json_data.iteritems(): #key is datetime string, value is a dictionary of {route name, [bus instance data]}
			if time_str >= start_time_str and time_str <= end_time_str: #make sure it's in this time interval
				for route, bus_list in route_data.iteritems():
					for bus_data in bus_list:
						# print bus_data
						if bus_data['key'] == bus_id:
							bus_instance_data.append((time_str, bus_data)) #tuple (time, bus_data)

		bus_instance_data = sorted(bus_instance_data, key=lambda item: item[0]) #sort by time
		pprint.pprint(bus_instance_data)

	else:
		print 'Bus data not available.'

	return bus_instance_data

def load_json_file():
	if os.path.exists(file_name):
		with open(file_name) as f:
			json_data = json.load(f) # dict {datetime, dict {route name, [bus instance data]}}
			f.close()
			return json_data
	return None


if __name__ == '__main__':
	get_bus_instance_data("f532dcd5-4998-41b1-af0d-7b01e33da8f0", "13-11-22-11-46-00", "13-11-22-11-47-50")

