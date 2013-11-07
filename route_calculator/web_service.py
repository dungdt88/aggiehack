import json, random
import datetime
from flask import Flask
from flask import request
from flask import jsonify

#from flask import Response

#from json import JSONEncoder

app = Flask(__name__)

start_node = {'name': 'HEB', 'long':'-96.31823300', 'lat':'30.61206100'}
node1 = {'name':'MSC', 'long':'-96.33965217', 'lat':'30.61393756'}
node2 = {'name': 'Community Center', 'long':'-96.34027000', 'lat': '30.62722200'}
node3 = {'name': 'Trigon', 'long':'-96.33926200', 'lat': '30.61355700'}
node4 = {'name': 'ETB', 'lat':'30.630231', 'long': '-96.338425'}
end_node = {'name': 'Peppertree','long':'-96.29545600', 'lat':'30.59359200'}

data = [node1, node2, node3, node4, start_node, end_node]
trans_type = ['walking', 'bus']

def dump_result():
	num_of_results = random.randint(2,3)
	results = []
	for j in range(num_of_results):
		num_of_steps = random.randint(2,3)
		steps = []
		for i in range(num_of_steps):
			start = data[random.randint(0,len(data)-1)]
			end = data[random.randint(0,len(data)-1)]
			typn = trans_type[random.randint(0,1)]
			duration = random.uniform(10,1000)
			start_time = datetime.datetime.now()
			one_step = {'start': start, 'end':end, 'type':typn, 'duration': duration, "start_time": start_time}

			#print one_step
			steps.append(one_step)

		results.append(steps)

	return {"results": results, "status": "OK"}

@app.route('/lat1/<lat1>/long1/<long1>/lat2/<lat2>/long2/<long2>/time/<start_time>')
def api_long(lat1, long1, lat2, long2, start_time):
    #req = 'lat1: ' + lat1 + ' long1:' + long1 + ' lat2: ' + lat2 + 'long2: ' + long2 + 'time: ' + start_time

    #data validation

    message = dump_result()
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run()
    #dump_result()