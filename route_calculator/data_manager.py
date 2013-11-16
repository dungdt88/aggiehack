import data_structure
from data_structure import *
from constants import *
from db_util import *
import igraph
from igraph import *
import os.path
import cPickle


class DataManager:
    def __init__(self):
        self.bus_steps = initialize_bus_steps()
        self.walking_times = initialize_walking_times()
        self.locations = initialize_locations()


    def get_next_states(self, current_state, goal_node):
        next_bus_steps = self.get_next_bus_steps(current_state)
        next_walking_steps = self.get_next_walking_steps(current_state, goal_node)
        
        next_steps = (next_bus_steps + next_walking_steps)
        next_states = []

        for step in next_steps:
            # step.print_info()
            new_node = step.end_node
            new_state = State(new_node, step.end_time, step, current_state)
            next_states.append(new_state) 

        return next_states


    def get_next_bus_steps(self, current_state):
        next_steps = [i for i in self.bus_steps if i.start_node.id == current_state.node.id and i.start_time >= current_state.arrived_time]
        return next_steps


    def get_next_walking_steps(self, current_state, goal_node):
        next_steps = []
        # get next nodes of starting node
        if current_state.node.id == START_NODE_ID: 
            for next_node in self.locations:
                dist = util.distance(next_node.latitude, next_node.longitude, current_state.node.latitude, current_state.node.longitude)
                if dist <= MAX_DISTANCE:
                    moving_time = util.get_moving_time(dist, WALKING_VELOCITY)
                    step = Step(current_state.node, next_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, moving_time), WALKING_TYPE)
                    next_steps.append(step)
        else:
            times = [i for i in self.walking_times if i.start_loc_id == current_state.node.id] 
            for t in times:
                moving_time = t.time
                next_node = [i for i in self.locations if i.id == t.end_loc_id][0]
                step = Step(current_state.node, next_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, moving_time), WALKING_TYPE)
                next_steps.append(step)

        # add step to goal_node
        distance = util.distance(current_state.node.latitude, current_state.node.longitude, goal_node.latitude, goal_node.longitude)
        to_goal_time = util.get_moving_time(distance, WALKING_VELOCITY)
        to_goal_step = Step(current_state.node, goal_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, to_goal_time), WALKING_TYPE)
        next_steps.append(to_goal_step)

        return next_steps

# Utility functions outside DataManager class
def initialize_bus_steps():
    #load from pickle file if already exists
    file_name = "pickle_files/bus.pkl"
    if os.path.exists(file_name):
        pfile = open(file_name, 'rb')
        bus_steps = cPickle.load(pfile)
        pfile.close()
    else:
        pfile = open(file_name, 'wb')
        sql_helper = SqlHelper()
        bus_steps = sql_helper.get_all_steps_by_bus()
        cPickle.dump(bus_steps, pfile)
        pfile.close()

    return bus_steps

def initialize_walking_times():
    #load from pickle file if already exists
    file_name = "pickle_files/walk.pkl"
    if os.path.exists(file_name):
        pfile = open(file_name, 'rb')
        walking_times = cPickle.load(pfile)
        pfile.close()
    else:
        pfile = open(file_name, 'wb')
        sql_helper = SqlHelper()
        walking_times = sql_helper.get_all_walking_times()
        cPickle.dump(walking_times, pfile)
        pfile.close()

    return walking_times

def initialize_locations():
    #load from pickle file if already exists
    file_name = "pickle_files/location.pkl"
    if os.path.exists(file_name):
        pfile = open(file_name, 'rb')
        locations = cPickle.load(pfile)
        pfile.close()
    else:
        pfile = open(file_name, 'wb')
        sql_helper = SqlHelper()
        locations = sql_helper.get_all_nodes()

        cPickle.dump(locations, pfile)
        pfile.close()

    return locations

# def process_duration(duration):
#     days, seconds = duration.days, duration.seconds
#     hours = days * 24 + seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = seconds % 60
#     #print '{} minutes, {} hours'.format(minutes, hours)
#     return {'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds}


#get path from start to goal
def get_path(final_state):
    path = []
    prv = final_state
    while prv.previous_state != None:
        path.append(prv.previous_step)
        prv = prv.previous_state

    path.reverse()

    string = ""
    for i, p in enumerate(path):
        s = p.start_node.name
        e = p.end_node.name
        st = p.start_time
        et = p.end_time
        type = p.type
        
        string += s + ', ' + e + ', ' + str(st) + ', ' + str(et) + ', ' + type + "\n"

    return string
