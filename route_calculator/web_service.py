import random
import datetime
from constants import *
from flask import Flask
from flask import request
from flask import jsonify

#crap import
import RouteCalculator
from constants import *
from data_structure import *
from db_util import *
from RouteCalculator import *
from time import clock

import pytz, time, os

os.environ['TZ'] = 'US/Central'
time.tzset()

local_timezone = pytz.timezone("US/Central")

app = Flask(__name__)


#validate time input
def validate_datetime(s_time):
    now = datetime.datetime.now()
    if s_time < now:
        return False
    end_of_the_day = datetime.datetime(s_time.year, s_time.month, s_time.day, 23, 59, 59)
    if s_time > end_of_the_day:
        return False
    return True

#validate coordinate input
def validate_long_lat(longitute, latitude):
    if float(longitute) < LONGTITUDE_LEFT_BOUND or float(longitute) > LONGTITUDE_RIGHT_BOUND:
        print 'long exceed'
        return False
    if float(latitude) > LATITUDE_UPPER_BOUND or float(latitude) < LATITUDE_LOWER_BOUND:
        print 'lat exceed'
        return False
    return True


#convert pathlist to json for web service
def convert_results_to_json(path_list):
    results_list = []
    for path in path_list:
        steps = []
        for i, state in enumerate(path):
            if state.previous_step != None:
                p  = state.previous_step
                start = {'name': p.start_node.name, 'long': str(p.start_node.longitude), 'lat': str(p.start_node.latitude)}
                end = {'name': p.end_node.name, 'long': str(p.end_node.longitude), 'lat': str(p.end_node.latitude)}
                start_time = local_timezone.localize(p.start_time)
                time_string = start_time.strftime("%A %Y-%m-%d %H:%M:%S %Z%z")
                duration = (p.end_time - p.start_time).seconds
                typn = p.type
                bus_number = ""
                if typn is not WALKING_TYPE:
                    bus_number = typn
                    typn = BUS_TYPE
                one_step = {'start': start, 'end':end, 'type':typn, 'bus_number': bus_number, 'duration': duration, "start_time": time_string}

                steps.append(one_step)
        results_list.append(steps)
    return results_list


#Call AI engine to get the shortest path
def get_results(lat1, long1, lat2, long2, start_time):

    start_node = Node(-1, "Start", lat1, long1) #ETB
    goal_node = Node(-2, "End", lat2, long2)

    start = clock();
    calculator = RouteCalculator()
    end = clock();
    print "Finish initialization in %6.3f seconds" % (end - start)

    start = clock();
    path_list = calculator.search(start_node, goal_node, start_time, K_SHORTEST)
    end = clock();
    print "Finish searching in %6.3f seconds" % (end - start)
    
    if len(path_list) == 0:
        return {"results": "None", "status": "404"}
    else:
        results = convert_results_to_json(path_list)
        return {"results": results, "status": "OK"}


@app.route('/orgLat/<lat1>/orgLong/<long1>/desLat/<lat2>/desLong/<long2>/time/<start_time>')
def api_long(lat1, long1, lat2, long2, start_time):
    #req = 'lat1: ' + lat1 + ' long1:' + long1 + ' lat2: ' + lat2 + 'long2: ' + long2 + 'time: ' + start_time

    #data validation
    # validate latitude and longitude
    if (not validate_long_lat(long1, lat1)) or (not validate_long_lat(long2, lat2)):
        err = "Longitude and latitude exceeding boundary"
        return not_found(err)

    s_time = datetime.datetime.fromtimestamp(int(start_time))
    #validate datetime
    #time must between now and end of the day

    # comment temporary for testing
    # if not validate_datetime(s_time):
    #     error = "Date time is out of boundary"
    #     return not_found(error)

    # print lat1, long1, lat2, long2, s_time

    message = get_results(float(lat1), float(long1), float(lat2), float(long2), s_time)
    resp = jsonify(message)
    resp.status_code = 200
    return resp


#handle not found error
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': error if error is not None else 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


#handle internal server error
@app.errorhandler(500)
def internal_error(error=None):
    message = {
            'status': 500,
            'message': 'Fuck up: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp


#main
if __name__ == '__main__':
    #print validate_datetime(str(datetime.datetime.now()))
    app.run(host='0.0.0.0')
    #dump_result()
