import MySQLdb
import urllib2
import json
from BeautifulSoup import BeautifulSoup as bs
from pprint import pprint
import time 
import datetime
from time import strptime, strftime

# global 
# route_pages = ['26']
route_pages = ['01', '02', '04', '04N', '05', '06', '08', '12', '15', '22', '26', '27', '31', '33', '34', '35', '36']
all_bus_stops = []
schedule = []
bad_data = ['\n', 'No Service Is Scheduled For This Date']
blanks = ['&nbsp;', '\n']

# get data from each tamu bus schedule page
for route_page in route_pages:

	bus_page = urllib2.urlopen('http://transport.tamu.edu/busroutes/Route' + route_page + '.aspx')

	data =  bs(bus_page)

	route_bus_stops = []
	

	geo_data = data.find('input', {'id': 'routeDataHiddenField'})['value']
	geo_json = json.loads(geo_data)
	geo_list = geo_json['pattern']

	print route_page
	print len(geo_list)
	print [x['key'] for x in geo_list]

	for table in data.findAll('table'):
		#get bus stop names
		for tr in table.findAll('tr')[1]:
			route_bus_stops.append(tr.string)
			if tr.string not in all_bus_stops and tr.string not in bad_data:
				all_bus_stops.append(tr.string)
		
		#get schedule
		for tr in table.findAll('tr')[2:]:
			for td in tr.findAll('td'):
				if td.string not in blanks and td.nextSibling.string not in blanks:
					schedule.append((route_bus_stops[tr.index(td)], td.string, route_bus_stops[tr.index(td.nextSibling)], td.nextSibling.string, route_page))
					print route_bus_stops[tr.index(td)], td.string, route_bus_stops[tr.index(td.nextSibling)], td.nextSibling.string, route_page
	print
	
print 'Total bus stops:', len(all_bus_stops)
print all_bus_stops
print 'Schedule:', len(schedule)
# print pprint(schedule)



# db calls
db = MySQLdb.connect("localhost", "testuser", "test606", "aggiehack")
cursor = db.cursor()

for loc in all_bus_stops:

	# check if location exists, if not then insert
	sql = "SELECT * FROM location WHERE name = %s" 
	cursor.execute(sql, loc)

	if cursor.fetchone() == None:
			sql = "INSERT INTO location (name, longitude, latitude) VALUES (%s, %s, %s)"
			cursor.execute(sql, (db.escape_string(loc), 0.0, 0.0))
			db.commit()

# get all locations
sql = "SELECT id, name FROM location ORDER BY id"
cursor.execute(sql)

all_loc = {} # {name: id}

for loc in cursor.fetchall(): #return list of list
	all_loc[loc[1]] = loc[0]

for item in schedule:
	start_loc = all_loc[item[0]]
	start_time = datetime.date.today().strftime("%y-%m-%d") + ' ' + strftime("%H:%M:%S", time.strptime(item[1], "%I:%M %p")) 
	end_loc = all_loc[item[2]]
	end_time = datetime.date.today().strftime("%y-%m-%d") + ' ' + strftime("%H:%M:%S", time.strptime(item[3], "%I:%M %p")) 
	route = item[4]

	# print start_time, end_time

	sql = "INSERT INTO Schedule (start_loc_id, end_loc_id, start_time, end_time, route) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(sql, (start_loc, end_loc, start_time, end_time, route))
	db.commit()

db.close()
