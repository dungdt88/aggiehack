import MySQLdb
import time 
import datetime
from time import strptime, strftime

walking_threshold = 1800 #15 mins

def distance_gmap(orig_coord, dest_coord):
	# print orig_coord, dest_coord
	import json as simplejson, urllib

	# driving vs. walking
	#url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	
	result= simplejson.load(urllib.urlopen(url))
	distance = result['rows'][0]['elements'][0]['distance']['value']
	return distance


def moving_time_gmap(orig_coord, dest_coord):
	# print orig_coord, dest_coord
	import json as simplejson, urllib
	
	# driving vs. walking
	#url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	
	result= simplejson.load(urllib.urlopen(url))
	moving_time = result['rows'][0]['elements'][0]['duration']['value']
	return moving_time


if __name__ == '__main__':
	# db calls
	db = MySQLdb.connect("localhost", "testuser", "test606", "aggiehack")
	cursor = db.cursor()

	# get all locations
	sql = "SELECT id, latitude, longitude FROM location ORDER BY id"
	cursor.execute(sql)

	all_loc = []
	for loc in cursor.fetchall(): #return list of list
		all_loc.append(loc)

	# print all_loc

	for loc in all_loc:
		if all_loc.index(loc) < len(all_loc)-1:
			next_loc = all_loc[all_loc.index(loc) + 1]
			id1 = loc[0]
			id2 = next_loc[0]
			lat1 = float(loc[1])
			lat2 = float(next_loc[1])
			long1 = float(loc[2])
			long2 = float(next_loc[2])

			# print lat1, long1, lat2, long2

			# distance_gmap
			dist = distance_gmap((lat1, long1), (lat2, long2))

			# moving_time_gmap
			moving_time = moving_time_gmap((lat1, long1), (lat2, long2))
	
			print dist, moving_time

			if moving_time <= walking_threshold:
				print moving_time

				# only insert when location not exists
				sql = "SELECT * FROM distance WHERE start_loc_id = %s AND end_loc_id = %s" 
				cursor.execute(sql, (id1, id2))

				if cursor.fetchone() == None:
					sql = "INSERT INTO distance (start_loc_id, end_loc_id, time, distance) VALUES (%s, %s, %s, %s)"
					cursor.execute(sql, (id1, id2, moving_time, dist))
					db.commit()
