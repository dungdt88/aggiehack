import MySQLdb
import urllib2
import json
from BeautifulSoup import BeautifulSoup as bs
from pprint import pprint
import time 
import datetime
from time import strptime, strftime
import sys
sys.path.insert(0, '../route_calculator/')
import constants
from constants import *
import os
import data_manager
from data_manager import *

# global 
route_pages = ['01', '02', '04', '04N', '05', '06', '08', '12', '15', '22', '26', '27', '31', '33', '34', '35', '36']
bad_data = ['\n', 'No Service Is Scheduled For This Date']
blanks = ['&nbsp;', '\n']

def get_data_from_page(schedule):
        # get data from each tamu bus schedule page
        for route_page in route_pages:

                bus_page = urllib2.urlopen('http://transport.tamu.edu/busroutes/Route' + route_page + '.aspx')

                data =  bs(bus_page)

                # store schedule for this particular route
                route_bus_stops = []

                # get all bus stops and their schedule
                for table in data.findAll('table'):
                        #get bus stop names
                        for tr in table.findAll('tr')[1]:
                                route_bus_stops.append(tr.string.strip())
                        
                        #get schedule
                        for tr in table.findAll('tr')[2:]:
                                for td in tr.findAll('td'):
                                        if td.string not in blanks and td.nextSibling.string not in blanks:
                                                schedule.append((route_bus_stops[tr.index(td)], td.string, route_bus_stops[tr.index(td.nextSibling)], td.nextSibling.string, route_page))
                                                # print route_bus_stops[tr.index(td)], td.string, route_bus_stops[tr.index(td.nextSibling)], td.nextSibling.string, route_page
                print
                
        print 'Schedule:', len(schedule)
        # print pprint(schedule)


def update_db(schedule):
        f = open('log/' + datetime.date.today().strftime("%y-%m-%d") + '.txt', 'w')
        has_error = False

        db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DBNAME)
        cursor = db.cursor()

        # get all locations
        all_loc = {} # {name: id}
        sql = "SELECT id, name FROM location ORDER BY id"
        cursor.execute(sql)
        for loc in cursor.fetchall(): #return list of list
                all_loc[loc[1]] = loc[0]

        sql = "DELETE FROM schedule"
        cursor.execute(sql)
        db.commit()

        # populate table schedule
        count = 0
        for item in schedule:
                if item[0] in all_loc and item[2] in all_loc:
                        start_loc_id = all_loc[item[0]]
                        start_time = datetime.date.today().strftime("%y-%m-%d") + ' ' + strftime("%H:%M:%S", time.strptime(item[1], "%I:%M %p")) 
                        end_loc_id = all_loc[item[2]]
                        end_time = datetime.date.today().strftime("%y-%m-%d") + ' ' + strftime("%H:%M:%S", time.strptime(item[3], "%I:%M %p")) 
                        route = item[4]

                        # print start_loc_id, end_loc_id, start_time, end_time, route
                        
                        sql = "INSERT INTO schedule (start_loc_id, end_loc_id, start_time, end_time, route) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (start_loc_id, end_loc_id, start_time, end_time, route))
                        db.commit()

                        f.write(str(start_loc_id) + ', ' + str(end_loc_id) + ', ' + start_time + ', ' + end_time + ', ' + route + '\n')
                        count = count + 1
                else:
                        if item[0] not in all_loc:
                                f.write(item[0] + ' is not in existing location list\n')
                        if item[2] not in all_loc:
                                f.write(item[2] + ' is not in existing location list\n')

        if has_error:
                f.write('Error detected!!')
        else:
                f.write('Successful!! ' + str(count) +' records. \n')
        db.close()

def generate_pickle_files():
	rel_path = '../route_calculator/'
	bus_file = rel_path + PICKLE_FILE_BUS
	walk_file = rel_path + PICKLE_FILE_WALK
	location_file = rel_path + PICKLE_FILE_LOCATION
	
	delete_file(bus_file)
	delete_file(walk_file)
	delete_file(location_file)

	initialize_bus_steps(bus_file)
	initialize_walking_times(walk_file)
	initialize_locations(location_file)

	print 'Successfully writing to pickle files.'

def delete_file(file_name):
	try:
		os.remove(file_name)
	except OSError, e:
		print ("Warning: %s - %s." % (e.filename,e.strerror))

if __name__ == '__main__':
        # schedule = []
        # get_data_from_page(schedule)
        # update_db(schedule)
        generate_pickle_files()
