__author__ = 'DucNguyen'

import util
from datetime import datetime

# Find the segment that a location (lat, lng) belongs to.
# Then return infor of ending shape of that segment
def get_next_shape_info(lat, lng, list_shapes):
    #ret_next_shape_id = -1
    ret_distance_remain = -1
    ret_next_seq = -1

    min_deviation = 100000
    next_id = -1
    for i in range(len(list_shapes)-1):
        dev = calc_deviation(lat, lng, list_shapes[i], list_shapes[i+1])
        if dev < min_deviation:
            min_deviation = dev
            next_id = i + 1

    if next_id > -1:
        next_shape = list_shapes[next_id]
        #ret_next_shape_id = next_shape[0] # id
        ret_distance_remain = util.distance(lat, lng, next_shape[1], next_shape[2])
        ret_next_seq = next_shape[5]

    return ret_distance_remain, ret_next_seq


def calc_deviation(lat, lng, start_shape, end_shape):
    return   (util.distance(lat, lng, start_shape[1], start_shape[2]) \
           + util.distance(lat, lng, end_shape[1], end_shape[2]) \
           - util.distance(start_shape[1], start_shape[2], end_shape[1], end_shape[2]))\
           / util.distance(start_shape[1], start_shape[2], end_shape[1], end_shape[2])


# list_live_data = [(time, {key_bus_id, lat, lng, next_stop, estDepart})]
# list_shapes = [(shape_id, lat, lng, x, y, seq, distance)]
def process_live_route_data(list_live_data, list_shapes):
    ret_data_items = []
    i = 0
    while i < len(list_live_data):
        live_data_item = list_live_data[i]
        next_seq = get_next_shape_info(live_data_item[1]['lat'], live_data_item[1]['lng'], list_shapes)[1]
        result = process_to_pass_next_seq(list_live_data, i, list_shapes, next_seq)
        print("running ...")
        if result is not None:
            i = result[1]
            if i != 0:
                ret_data_items.append(result[0])
            continue
        else:
            break

    return ret_data_items


def process_to_pass_next_seq(list_live_data, cur_live_data_item_index, list_shapes, cur_seq):
    cur_live_data_item = list_live_data[cur_live_data_item_index]
    i = cur_live_data_item_index
    while i < len(list_live_data)-1:
        i += 1
        live_data = list_live_data[i]
        next_seq = get_next_shape_info(live_data[1]['lat'], live_data[1]['lng'], list_shapes)[1]
        if next_seq != cur_seq:
            start_seq = cur_seq
            end_seq = next_seq
            date = cur_live_data_item[0][:8] # cut from string 'yy-MM-dd-hh-mm-ss'
            #start_time = cur_live_data_item[0][9:18] # cut from string 'yy-MM-dd-hh-mm-ss'
            start_time = cur_live_data_item[0]
            end_time = live_data[0]

            start_timetype = datetime.strptime(start_time, "%y-%m-%d-%H-%M-%S")
            end_timetype   = datetime.strptime(end_time, "%y-%m-%d-%H-%M-%S")
            #return (end_timetype - start_timetype).seconds

            #duration = get_difft_time(end_time, cur_live_data_item[0])
            duration = (end_timetype - start_timetype).seconds
            return [[start_seq, end_seq, start_timetype, duration], i]
    return None


if __name__ == '__main__':
    print("start")

    # list_shapes = [(shape_id, lat, lng, x, y, seq, distance)]
    list_shapes = [(123, 30.569814, -96.363036, 1, 2, 0, 100)
                 , (124, 30.568814, -96.364036, 1, 2, 1, 100)
                 , (125, 30.567814, -96.365036, 1, 2, 2, 100)
                 , (126, 30.566814, -96.366036, 1, 2, 3, 100)
                 , (127, 30.565814, -96.367036, 1, 2, 4, 100)]
    lat = 30.566114
    lng = -96.365836

    print(get_next_shape_info(lat, lng, list_shapes))
    #list_live_data = [ ("13-11-11-10-19-12", {'key_bus_id': "key_bus_id", 'lat':30.569714, 'lng':-96.363136, 'next_stop':"next_stop", 'estDepart':"estDepart"})
    #                  ,("13-11-11-10-19-22", {'key_bus_id': "key_bus_id", 'lat':30.568714, 'lng':-96.364136, 'next_stop':"next_stop 1", 'estDepart':"estDepart 1"})
    #                  ,("13-11-11-10-19-32", {'key_bus_id': "key_bus_id", 'lat':30.567714, 'lng':-96.365136, 'next_stop':"next_stop 2", 'estDepart':"estDepart 2"})
    #                  ,("13-11-11-10-19-42", {'key_bus_id': "key_bus_id", 'lat':30.566714, 'lng':-96.366136, 'next_stop':"next_stop 3", 'estDepart':"estDepart 3"})
    #                ] # [(time, {key_bus_id, lat, lng, next_stop, estDepart})]
    #print(process_live_route_data(list_live_data, list_shapes))

    print("end")

