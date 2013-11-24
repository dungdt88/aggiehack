import KalmanFilter
from KalmanFilter import *
import data_processor
from data_processor import *
import sample_data_generator
from sample_data_generator import *
import datetime
from datetime import datetime, date, time

sample_route_name = "15"
sample_num_intervals = 40
sample_current_time_str = "13-11-23-14-10-00"


def predict_arrival_time(bus_data, current_time, goal_node):
	# call other function to get distance remaining and list of segments to goal
	distance_remaining = 0
	segments_remaining = []

	# get estimated arrival time at the next turn using Kalman Filter
	arrival_time = get_estimated_arrival_time_at_next_turn(bus_data, current_time, distance_remaining)
	
	# get estimated delta t on all the remaining segments
	for segment in segments_remaining:
		arrival_time = get_estimated_arrival_time_each_segment(arrival_time, segment)
	
	return arrival_time

def get_estimated_arrival_time_at_next_turn(bus_data, current_time, distance_remaining):
	delta_t = 0.0
	velocity = get_estimated_velocity(bus_data, current_time)
	if velocity > 0:
		delta_t = distance_remaining / velocity

	return util.add_secs(current_time, delta_t)

def get_bus_xy_coord_list(bus_data, current_time, num_intervals):
	temp = [i for i in bus_data if i[0] <= current_time.strftime("%y-%m-%d-%H-%M-%S")]
	temp = temp[len(temp)-num_intervals : len(temp)]

	xy_coords = []
	for i in temp:
		x = i[1]
		y = i[2]
		print i[0], x, y
		xy_coords.append([x, y])
	return xy_coords

def get_estimated_velocity(bus_data, current_time):

	temp_xy_list = get_bus_xy_coord_list(bus_data, current_time, sample_num_intervals+1)
	# print len(temp_xy_list)

	# initial_xy = temp_xy_list[len(temp_xy_list)-1] #initial is the last item
	# measurements = temp_xy_list[:len(temp_xy_list)-1] #the rest

	# print len(measurements)
	# print initial_xy

	measurements = [[11.5631105652, 5.91252278752], 
					[11.4441717806, 6.24034187227],
					[11.5205721048, 6.3403544744], 
					[11.3376722682, 6.56816095702], 
					[11.156887513, 6.60816599787], 
					[11.1186075473, 6.63483602511]]
	initial_xy = [10.8122506531, 6.97154511894]

	dt = 60

	x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
	u = matrix([[0.], [0.], [0.], [0.]]) # external motion 

	P =  matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,100.,0.],[0.,0.,0.,100.]])# initial uncertainty
	F =  matrix([[1.,0.,dt,0.],[0.,1.,0.,dt],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
	H =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
	R =  matrix([[1.,0.],[0.,1.]])# measurement uncertainty
	I =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])# identity matrix

	result = filter(measurements, x, u, P, F, H, R, I)

	vx = result.value[2][0]
	vy = result.value[3][0]
	print vx, vy
	v = math.hypot(vx, vy)
	print "v=", v, v*1000
	return v


def get_estimated_arrival_time_each_segment(start_time, segment):
	delta_t = 120 #seconds

	#TODO: build linear regression model and find delta_t spent on this segment

	return util.add_secs(start_time, delta_t)


def test():
    shape = get_route_shape(sample_route_name)
    bus_data = get_bus_instance_data(sample_bus_id, sample_start_time_str, sample_end_time_str)

    goal_node = Node(-1, "End at MSC", 30.612771,-96.342081) 
    current_time = datetime.strptime(sample_current_time_str, "%y-%m-%d-%H-%M-%S") 

    print "Current time:", current_time
    arrival_time = predict_arrival_time(bus_data, current_time, goal_node)


if __name__ == '__main__':
	test()
