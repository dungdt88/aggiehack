import os
import json
import pprint
import string
import db_util
from db_util import *

sample_route_name = "15" # hard code route name for now to get sample data
shapes_file = "../data/TS/shapes.txt"
trips_file = "../data/TS/trips.txt"

def replace_redundant_char(line):
	line = line.replace('\n', '')
	line = line.replace('\r', '')
	return line

def build_route_shapes(route_shape_dict):
	if os.path.exists(trips_file) and os.path.exists(shapes_file):
		sql_helper = SqlHelper()
		routes = sql_helper.get_all_routes()

		with open(trips_file, 'r') as tf, open(shapes_file, 'r') as sf:
			shape_dict = {}
			for i, line in enumerate(sf):
				if i > 0:
					line = replace_redundant_char(line)
					shape_item = line.split(',')
					shape_id = shape_item[0]

					x, y = util.get_xy_coord(shape_item[1], shape_item[2])
					shape_tuple = (shape_item[0], shape_item[1], shape_item[2], x, y, shape_item[3], shape_item[4])

					if shape_id in shape_dict:
						shapes = shape_dict[shape_id]
						shapes.append(shape_tuple)
					else:
						shapes = []
						shapes.append(shape_tuple)
						shape_dict[shape_id] = shapes
			sf.close()
			

			for i, line in enumerate(tf):
				if i > 0:
					line = replace_redundant_char(line)
					trip_item = line.split(',')
					route_id = trip_item[0]
					shape_id = trip_item[3]
					
					found = [i for i in routes if i[0]==route_id]
					if len(found) > 0:
						if shape_id in shape_dict:
							route_name = found[0][1]
							route_shape_dict[route_name] = shape_dict[shape_id]
			tf.close()



def get_route_shapes(route_name):
	
	route_shape_dict = {} #dictionary {route_id, [(shape_id, lat, long, x, y, sequence, distance)]}
	build_route_shapes(route_shape_dict) 

	shapes = [] # [(shape_id, lat, long, x, y, sequence, distance)]
	if route_name in route_shape_dict:
		shapes = sorted(route_shape_dict[route_name], key=lambda item: int(item[5])) # sort list by sequence
	return shapes


if __name__ == '__main__':

	shapes = get_route_shapes(sample_route_name)
	print shapes
	print len(shapes)