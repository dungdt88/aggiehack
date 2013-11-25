import KalmanFilter
from KalmanFilter import *
import data_processor
from data_processor import *
import os
import live_data_manager
import util

NUMBER_OF_MEASUREMENTS = 10
INFINITY = 10000

def run_predictor():
    running_list = [] #only locations on the current segment
    # prev_velocity = 0
    shape = get_route_shape("15")
    file_path = "live_data/bus_data.txt"

    if os.path.exists(file_path):
        with open(file_path, 'r') as data_file:
            for i, line in enumerate(data_file):
                if i < 20: #TODO: remove this. Run first 20 lines for testing only
                    line_items = line.split(' ')
                    current_time = util.from_str_to_datetime(line_items[0] + ' ' + line_items[1][:8], "%Y-%m-%d %H:%M:%S") #2013-11-24 21:30:17.120
                    current_time = current_time - datetime.timedelta(hours = 6) # adjust to local time

                    lng = line_items[2]
                    lat = line_items[3]

                    print current_time, lat, lng

                    dist_remain = update_running_list(running_list, lat, lng, shape)
                    velocity = predict(running_list)

                    if velocity > 0:
                        new_time = util.add_secs(current_time, get_time_remaining(velocity, dist_remain))
                        print "Predict time to next turn: %s\n" % (new_time)
                    else:
                        print "Can't predict time due to no movement.\n"

            data_file.close()

def update_running_list(running_list, lat, lng, shape):
    # check which sequence this lat, long belongs to, if stay on the same sequence
    # 	running_list.append (x, y, lat, long, sequence)
    # if not
    # 	clear running_list
    # 	running_list.append (x, y, lat, long, sequence)
    # calculate dist_remain
    # return dist_remain
    if len(running_list) == 0:
        cur_seq = 0
        seq = 0
    else:
        cur_seq = int(running_list[len(running_list)-1][4])
        seq = live_data_manager.get_seq_from_lat_lng(lat, lng, shape, cur_seq, cur_seq + 4)
    x, y = util.get_xy_coord(lat, lng)
    dist_remain = util.distance(lat, lng, shape[seq+1][1], shape[seq+1][2])
    if seq != cur_seq:
        running_list = []
        is_turn = True
    else:
        is_turn = False
    running_list.append((x, y, lat, lng, seq))
    return dist_remain
    #return running_list, is_turn, dist_remain


    #TODO: remove the following lines once this function is implemented. This is for testing only.
    #x, y = util.get_xy_coord(lat, lng)
    #running_list.append([x, y, lat, lng, 0])
    #return 0.0

def predict(running_list):
    if len(running_list) > 0:
        temp = []
        if len(running_list) > NUMBER_OF_MEASUREMENTS:
            temp = running_list[len(running_list)-NUMBER_OF_MEASUREMENTS:len(running_list)+1]  # the last k items in running_list
        else:
            temp = running_list[:]

        # if len(running_list) == 1:
        # 	v0 of Kalman = prev_velocity / 2
        print len(running_list), len(temp)
        measurements = []
        for item in temp:
            measurement = [item[0], item[1]]
            measurements.append(measurement)

        print measurements

        #set up Kalman Filter
        initial_xy = [running_list[0][0], running_list[0][1]]

        dt = 1

        x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
        u = matrix([[0.], [0.], [0.], [0.]]) # external motion

        P =  matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,100.,0.],[0.,0.,0.,100.]])# initial uncertainty
        F =  matrix([[1.,0.,dt,0.],[0.,1.,0.,dt],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
        H =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
        R =  matrix([[1.,0.],[0.,1.]])# measurement uncertainty
        I =  matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])# identity matrix

        #run Kalman filter
        result = filter(measurements, x, u, P, F, H, R, I)

        vx = result.value[2][0]
        vy = result.value[3][0]

        new_velocity = math.hypot(vx, vy)
        print "v=%s m/s, =%s mph" % (new_velocity*1000, new_velocity*1000*2.2369)

        # prev_velocity = new_velocity
        return new_velocity
    else:
        return 0.0

def get_time_remaining(velocity, dist_remain):
    if velocity > 0.0:
        return dist_remain/velocity
    return INFINITY


if __name__ == '__main__':
    run_predictor()
