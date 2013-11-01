import data_structure
from data_structure import *
from constants import *
from db_util import *

def get_next_steps(current_state):
    sql_helper = SqlHelper(HOST, DBNAME, USERNAME, PASSWORD)

    bus_steps = sql_helper.get_next_bus_steps(current_state)
    walking_steps = sql_helper.get_next_walking_steps(current_state)

    return (bus_steps + walking_steps)

#Generate possible states by consider possible ways to get from 1 States to available nodes around
def get_next_states(current_state):

    # get the nearest state in term of time cost
    next_steps = get_next_steps(current_state)
    next_states = [] 

    for step in next_steps:
        new_started_time = step.start_time
        new_arrived_time = new_started_time + (step.end_time - step.start_time)
        new_node = step.end_node
        new_state = State(new_node, current_state.goal_node, new_started_time, new_arrived_time, step, current_state)
        next_states.append(new_state) #push(new_state, (new_arrived_time - new_started_time)) #push to priority queue

    return next_states

#get path from start to goal
def get_path(final_state):
    prv = final_state
    path = []
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


