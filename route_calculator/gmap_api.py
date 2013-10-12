import util

def distance_gmap(node1, node2):
	# import json as simplejson, urllib

	# # driving vs. walking
	# #url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	# url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	
	# result= simplejson.load(urllib.urlopen(url))
	# print result
	# distance = result['rows'][0]['elements'][0]['distance']['value']

	return util.distance(node1[0], node1[1], node2[0], node2[1])


def moving_time_gmap(node1, node2):
	# import json as simplejson, urllib
	
	# # driving vs. walking
	# #url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	# url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	
	# result= simplejson.load(urllib.urlopen(url))
	# #print result['rows'][0]
	# moving_time = result['rows'][0]['elements'][0]['duration']['value']
	return util.distance(node1[0], node1[1], node2[0], node2[1])/10.0


# example 
if __name__ == '__main__':
	import time

	lat1 = 30.627977; lat2 = 30.674364; long1 = -96.334407; long2 = -96.369963
	
	# distance_gmap
	start_time = time.time()
	print( distance_gmap((lat1, long1), (lat2, long2)) )
	print time.time() - start_time, "meters"

	# moving_time_gmap
	start_time = time.time()
	print(moving_time_gmap((lat1, long1), (lat2, long2)) )
	print time.time() - start_time, "seconds"
