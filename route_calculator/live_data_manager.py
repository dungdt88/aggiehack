import json
import os
import data_processor
import sample_data_generator
import util

__author__ = 'DucNguyen'


#------------------------------------------------------------------------------------------
# INPUT:
#   running_list = [(x,y,lat,long,sequence)]
#   lat
#   long
#   shape = [(shape_id, lat, lng, x, y, seq, distance)] # ordered by seq
# OUTPUT:
#   running, is_turn, dist_remain
def update_running_list(running_list, lat, lng, shape):
    if len(running_list) == 0:
        cur_seq = 0
        seq = 0
    else:
        cur_seq = int(running_list[len(running_list)-1][4])
        seq = get_seq_from_lat_lng(lat, lng, shape, cur_seq, cur_seq + 4)
    x, y = util.get_xy_coord(lat, lng)
    dist_remain = util.distance(lat, lng, shape[seq+1][1], shape[seq+1][2])
    if seq != cur_seq:
        running_list = []
        is_turn = True
    else:
        is_turn = False
    running_list.append((x, y, lat, lng, seq))
    return running_list, is_turn, dist_remain


#------------------------------------------------------------------------------------------
# INPUT:
#   . list_live_data = [(time, {key_bus_id, lat, lng, nextStop, estDepart})]
# {key_bus#: [{"direction": "324", "nextStop": "Fish Pond", "route": "04N", "estDepart": "13:31"
#            , "occupancy": "0 %", "key": "3e239a54-b74e-4e7f-9010-b99ca1549224"
#            , "lat": "30.614", "lng": "-96.34162"}]
# }
# OUTPUT:
#   . {(start_bus_stop, end_bus_stop):[(start_time, duration)]}
BUS_NUMBER = '15'
def stat_duration_per_segment(ls_live_data):
    ret_dict = {}
    first_start_bus_stop = 'temp_bus_stop'
    first_end_bus_stop = None
    cur_start_bus_stop = first_start_bus_stop
    cur_end_bus_stop = None

    for live_data_item in ls_live_data:
        if live_data_item[1].has_key(BUS_NUMBER):
            next_bus_stop = live_data_item[1][BUS_NUMBER][0]['nextStop']
            if cur_end_bus_stop is None:
                cur_end_bus_stop = next_bus_stop
                first_end_bus_stop = next_bus_stop # for deleting first segment after complete process
                cur_start_time = live_data_item[0]
            if next_bus_stop != cur_end_bus_stop:
                cur_end_time = live_data_item[0]
                duration = util.get_difft_time(cur_end_time, cur_start_time)
                if not ret_dict.has_key((cur_start_bus_stop, cur_end_bus_stop)):
                    ret_dict[(cur_start_bus_stop, cur_end_bus_stop)] = [(cur_start_time, duration)]
                else:
                    ret_dict[(cur_start_bus_stop, cur_end_bus_stop)].append((cur_start_time, duration))
                # Reset values
                cur_start_bus_stop = cur_end_bus_stop
                cur_end_bus_stop = next_bus_stop
                cur_start_time = cur_end_time

    # delete 1st segment since it is incomplete
    del ret_dict[(first_start_bus_stop, first_end_bus_stop)]

    return ret_dict


def collect_bus_stop_in_route():
    return None

#------------------------------------------------------------------------------------------
def get_seq_from_lat_lng(latitude, longitude, shape, start_seq, end_seq):
    shape_Fisbol = ('',30.616315,-96.343419,0,0,0)
    min_dev = 1000000
    min_seq = -1
    numb_seq = len(shape)
    for i in range(start_seq, end_seq + 1):
        if i < numb_seq - 2:
            dev = calc_deviation(latitude, longitude, shape[i%numb_seq], shape[(i+1)%numb_seq])
            if i == 2: # with Fisbol shape: need special process
                dev_to_Fisbol = calc_deviation(latitude, longitude, shape[i%numb_seq], shape_Fisbol)
                dev_to_shape3 = calc_deviation(latitude, longitude, shape_Fisbol, shape[3])
                dev = dev_to_Fisbol if dev_to_Fisbol < dev_to_shape3 else dev_to_shape3
            if dev < min_dev:
                min_seq = i
                min_dev = dev
    return min_seq


#------------------------------------------------------------------------------------------
# Calculate distance between a location(lat, lng) with a segment
def calc_deviation(lat, lng, start_shape, end_shape):
    return  (util.distance(lat, lng, start_shape[1], start_shape[2]) \
           + util.distance(lat, lng, end_shape[1], end_shape[2]) \
           - util.distance(start_shape[1], start_shape[2], end_shape[1], end_shape[2]))\
           / util.distance(start_shape[1], start_shape[2], end_shape[1], end_shape[2])


#------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("start")

    #TASK: test update_running_list() function
    #1 Process Data:
    ls_live_data = []
    file_name = "../route_crawler/live_data/bus.json"
    if os.path.exists(file_name):
        with open(file_name) as f:
            ls_live_data = json.load(f) # [datetime, dict {route name, [bus instance data]}}
            f.close()

    #sample_route_name = "15" # hard code route name for now to get sample data
    #shape = data_processor.get_route_shape(sample_route_name)
    #print(shape)
    #
    ##2 Test update_running_list():
    #running_list = []
    #for live_data_item in ls_live_data:
    #    lat = live_data_item[0]
    #    lng = live_data_item[1]
    #    running_list = update_running_list(running_list, lat, lng, shape)[0]
    #    print running_list[len(running_list)-1]


    #TASK: test group_live_data_to_segment() function
    #file_name = "../route_crawler/live_data/bus.json"
    #sample_bus_id = "cb227902-a30c-4c00-b9c1-c3af9321769d"
    #sample_start_time_str = "13-11-23-08-00-00"
    #sample_end_time_str = "13-11-23-17-35-00"
    #
    #ls_live_data = sample_data_generator.get_bus_instance_data(sample_bus_id, sample_start_time_str, sample_end_time_str)
    result = stat_duration_per_segment(ls_live_data)
    for k in result.keys():
        print "key = ", k, " - value = ", result[k]



    print("end")