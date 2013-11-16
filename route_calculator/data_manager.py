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
        self.bus_graph = initialize_graph()
        self.walking_graph = initialize_walking_graph()
        self.nodes = initialize_nodes()


    def get_next_steps_and_durations(self, current_step, goal_node):
        bus_steps_and_durations = self.get_next_bus_steps_and_durations(current_step)
        walking_steps_and_durations = self.get_next_walking_steps_and_durations(current_step, goal_node)
        return (bus_steps_and_durations + walking_steps_and_durations)

    def get_next_bus_steps_and_durations(self, current_step):
        next_steps_and_durations = []
        #find all edges coming from current_step
        #for each edge: 
        #1. get target node of this edge, which is a step
        #2. total_time = edge's weight
        #3. append each tuple (new step, total_time) to next_steps

        #this line causes problem. Need to loop through all the vertices and check if a node has start_node.id == current_step.end_node.id and start_time > current_step.end_time
        #if so, we don't really need igraph, just save as a dictionary or list
        start_loc = self.bus_graph.vs.select(value=current_step) 
        print "Current", len(start_loc)
        current_step.print_info()
        if len(start_loc) > 0:
            edges = self.bus_graph.es.select(_source = start_loc[0].index)
            for e in edges:
                moving_time = e["duration"]
                print "Time", moving_time
                next_step = self.bus_graph.vs[e.target]["value"]
                step = Step(current_step.end_node, next_step.start_node, current_step.end_time, next_step.end_time, next_step.trans_type)
                step.print_info()
                next_steps_and_durations.append((step, moving_time))

        return next_steps_and_durations


    def get_next_walking_steps_and_durations(self, current_step, goal_node):
        next_steps_and_durations = []
        # get next nodes of starting node
        if current_step.end_node.id == START_NODE_ID: 
            for next_node in self.nodes:
                dist = util.distance(next_node.latitude, next_node.longitude, current_step.start_node.latitude, current_step.start_node.longitude)
                if dist <= MAX_DISTANCE:
                    moving_time = util.get_moving_time(dist, WALKING_VELOCITY)
                    step = Step(current_step.end_node, next_node, current_step.end_time, util.add_secs(current_step.end_time, moving_time), WALKING_TYPE)
                    next_steps_and_durations.append((step, moving_time))
        else:
            start_loc = self.walking_graph.vs.select(id=current_step.end_node.id)
            if len(start_loc) > 0:
                edges = self.walking_graph.es.select(_source = start_loc[0].index)
                for e in edges:
                    moving_time = e["duration"]
                    next_node_id = self.walking_graph.vs[e.target]["id"]
                    # print "Next", next_node_id, "Time", moving_time
                    next_node = [i for i in self.nodes if i.id == next_node_id][0]
                    step = Step(current_step.end_node, next_node, current_step.end_time, util.add_secs(current_step.end_time, moving_time), WALKING_TYPE)
                    step.print_info()
                    next_steps_and_durations.append((step, moving_time))


        # add step to goal_node
        distance = util.distance(current_step.end_node.latitude, current_step.end_node.longitude, goal_node.latitude, goal_node.longitude)
        to_goal_time = util.get_moving_time(distance, WALKING_VELOCITY)
        to_goal_step = Step(current_step.end_node, goal_node, current_step.end_time, util.add_secs(current_step.end_time, to_goal_time), WALKING_TYPE)
        next_steps_and_durations.append((to_goal_step, to_goal_time))

        return next_steps_and_durations

# Utility functions outside DataManager class
def initialize_graph():
    #load from pickle file if already exists
    file_name = "pickle_files/graph.pkl"
    if os.path.exists(file_name):
        pkl_file = open(file_name, 'rb')
        graph = cPickle.load(pkl_file)
    else:
        pkl_file = open(file_name, 'wb')
        sql_helper = SqlHelper()
        graph = Graph()

        # create vertices (steps) 
        all_steps = sql_helper.get_all_steps_by_bus()
        graph.add_vertices(len(all_steps))

        # create edges between vertices
        for idx, step in enumerate(all_steps):
           
            graph.vs[idx]["value"] = step
            for temp_idx, temp_step in enumerate(all_steps): #temp is next state
                if temp_step.start_node.id == step.end_node.id and temp_step.start_time > step.end_time:
                    graph.add_edges((idx, temp_idx))
                    graph.es[len(graph.es)-1]["duration"] = (temp_step.end_time - step.end_time).total_seconds() #total time = moving time + waiting time
                    print step.start_node.id, step.end_node.id, temp_step.start_node.id, temp_step.end_node.id, step.start_time, step.end_time, temp_step.start_time, temp_step.end_time, "by=", step.trans_type, temp_step.trans_type

        cPickle.dump(graph, pkl_file)
        pkl_file.close()

    summary(graph)
    return graph

def initialize_nodes():
    #load from pickle file if already exists
    file_name = "pickle_files/locations.pkl"
    if os.path.exists(file_name):
        pkl_file = open(file_name, 'rb')
        nodes = cPickle.load(pkl_file)
    else:
        pkl_file = open(file_name, 'wb')
        sql_helper = SqlHelper()
        nodes = sql_helper.get_all_nodes()
        cPickle.dump(nodes, pkl_file)
        pkl_file.close()
    return nodes


def initialize_walking_graph():
    #load from pickle file if already exists
    file_name = "pickle_files/walking_graph.pkl"
    if os.path.exists(file_name):
        pkl_file = open(file_name, 'rb')
        graph = cPickle.load(pkl_file)
    else:
        pkl_file = open(file_name, 'wb')
        graph = Graph()
        sql_helper = SqlHelper()

        all_times = sql_helper.get_all_walking_times()
        for t in all_times:

            idx_start = -1
            idx_end = -1

            if len(graph.vs) == 0:
                #if graph is empty then add new vertex
                graph.add_vertices(1)
                graph.vs[len(graph.vs)-1]["id"] = t.start_loc_id
                idx_start = len(graph.vs)-1
                print "add vertex", idx_start, "loc id", t.start_loc_id

                graph.add_vertices(1)
                graph.vs[len(graph.vs)-1]["id"] = t.end_loc_id
                idx_end = len(graph.vs)-1
                print "add vertex", idx_end, "loc id", t.end_loc_id
            else:
                #find index of vertex whose id = start_loc_id
                start_loc = graph.vs.select(id=t.start_loc_id)
                if len(start_loc) == 0:
                    graph.add_vertices(1)
                    graph.vs[len(graph.vs)-1]["id"] = t.start_loc_id
                    idx_start = len(graph.vs)-1
                    print "add vertex", idx_start, "loc id", t.start_loc_id
                else:
                    idx_start = start_loc[0].index

                #find index of vertex whose id = end_loc_id
                end_loc = graph.vs.select(id=t.end_loc_id)  
                if len(end_loc) == 0:
                    graph.add_vertices(1)
                    graph.vs[len(graph.vs)-1]["id"] = t.end_loc_id
                    idx_end = len(graph.vs)-1
                    print "add vertex", idx_end, "loc id", t.end_loc_id
                else:
                    idx_end = end_loc[0].index

            # create an edge between 2 nodes if not exists
            if idx_start != -1 and idx_end != -1:
                edges = graph.es.select(_within = [idx_start, idx_end]) 
                if len(edges) == 0:
                    graph.add_edges((idx_start, idx_end))
                    graph.es[len(graph.es)-1]["duration"] = t.time
                    print "add edge", idx_start, idx_end, t.time

        summary(graph)
        cPickle.dump(graph, pkl_file)
        pkl_file.close()

    return graph

# def process_duration(duration):
#     days, seconds = duration.days, duration.seconds
#     hours = days * 24 + seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = seconds % 60
#     #print '{} minutes, {} hours'.format(minutes, hours)
#     return {'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds}


#get path from start to goal
def get_path(final_state):
    if final_state == None:
        return None
        
    prv = final_state
    path = []
    path.append(prv)
    while prv.previous_step != None:
        path.append(prv.previous_step)
        prv = prv.previous_step

    path.reverse()

    steps = []
    for i, p in enumerate(path):
        start = {'name' : p.start_node.name, 'long' : str(p.start_node.longitude), 'lat' : str(p.start_node.latitude)}
        end = {'name' : p.end_node.name, 'long' : str(p.end_node.longitude), 'lat' : str(p.end_node.latitude)}
        start_time = p.start_time
        duration = (p.end_time - p.start_time).seconds

        #print duration

        typn = p.trans_type
        bus_number = ""
        if typn is not WALKING_TYPE:
            bus_number = typn
            typn = BUS_TYPE

        one_step = {'start': start, 'end':end, 'type':typn, 'bus_number': bus_number, 'duration': duration, "start_time": start_time}
        steps.append(one_step)

    # string = ""
    # for i, p in enumerate(path):
    #     s = p.start_node.name
    #     e = p.end_node.name
    #     st = p.start_time
    #     et = p.end_time
    #     typn = p.trans_type
        
    #     string += s + ', ' + e + ', ' + str(st) + ', ' + str(et) + ', ' + typn + "\n"
    
    return steps
