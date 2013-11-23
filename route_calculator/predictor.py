import KalmanFilter
from KalmanFilter import *
import data_processor
from data_processor import *
import sample_data_generator
from sample_data_generator import *
import datetime
from datetime import datetime, date, time

sample_num_intervals = 20
sample_current_time_str = "13-11-23-14-00-00"


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
	return temp[len(temp)-num_intervals : len(temp)]

def get_estimated_velocity(bus_data, current_time):

	temp_xy_list = get_bus_xy_coord_list(bus_data, current_time, sample_num_intervals+1)
	print len(temp_xy_list)

	initial_xy = temp_xy_list[len(temp_xy_list)-1] #initial is the last item
	measurements = temp_xy_list[:len(temp_xy_list)-1] #the rest

	print measurements
	print len(measurements)
	print initial_xy

	# measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
	# initial_xy = [4., 12.]

	dt = 0.1

	x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
	u = matrix([[0.], [0.], [0.], [0.]]) # external motion

	P =  matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,1000.,0.],[0.,0.,0.,1000.]])# initial uncertainty
	F =  matrix([[1.,0.,dt,0.],[0.,1.,0.,dt],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
	H =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
	R =  matrix([[0.1,0.],[0.,.1]])# measurement uncertainty
	I =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])# identity matrix

	# filter(measurements, x, u, P, F, H, R, I)
	return 0 #TODO: return velocity sqrt(x' sqr + y' sqr)



def get_estimated_arrival_time_each_segment(start_time, segment):
	delta_t = 120 #seconds

	#TODO: build linear regression model and find delta_t spent on this segment

	return util.add_secs(start_time, delta_t)


def test():
    shape = get_route_shape(sample_route_name)
    bus_data = get_bus_instance_data(sample_bus_id, sample_start_time, sample_end_time)
    goal_node = Node(-1, "End at MSC", 30.612771,-96.342081) 
    current_time = datetime.strptime(sample_current_time_str, "%y-%m-%d-%H-%M-%S") 

    print current_time
    arrival_time = predict_arrival_time(bus_data, current_time, goal_node)


if __name__ == '__main__':
	test()
