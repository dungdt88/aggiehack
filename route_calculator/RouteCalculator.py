import util 
import data_structure
import data_manager
import json, sys, random
from data_manager import *
from data_structure import *

from time import clock

class RouteCalculator:

    def __init__(self):
        self.data_manager = DataManager()

    def search(self, start_node, goal, start_time, k_shortest):
        path_list = [] # each list consists of path, which is a list of states
        start_state = State(start_node, start_time, None, None)
        path_found = self.a_search(start_state, goal, start_time)
        # path_found.print_info()
        path_list.append(path_found)

        potential_path_list = PriorityQueue()
        prev_prohibited_states = []
        
        for k in range(1, k_shortest): #from 1 to k
            
            if len(path_list) >= k:
                #remove each state of the final path from the graph
                temp_prohibited_states = []

                for spur_node in reversed(path_list[k-1]):
                    # print "Spur"
                    # spur_node.print_info()
                    temp_prohibited_states.append(spur_node)

                    prohibited_states = prev_prohibited_states
                    prohibited_states.append(spur_node)
                    # print "prohibited length", len(prohibited_states)

                    alternate_path = self.a_search(start_state, goal, start_time, prohibited_states)
                    # print "Alternate"
                    # alternate_path.print_info()

                    if potential_path_list.search(alternate_path) == False:
                        # print "Pushed"
                        path_cost = get_path_cost(alternate_path.get_last(), start_time)
                        potential_path_list.push(alternate_path, path_cost)

                if not potential_path_list.isEmpty(): 
                    path_found = potential_path_list.pop()
                    # path_found.print_info()
                    path_list.append(path_found)
                    prev_prohibited_states = prev_prohibited_states + temp_prohibited_states
            
        return path_list


    def a_search(self, start_state, goal, start_time, prohibited_states=[]):
        found = False
        resign = False
        pQueue = PriorityQueue()

        pQueue.push(start_state, 0)
        explored = []
        final_state = None

        count = 0
        while not found and not resign:
            count = count + 1

            if pQueue.isEmpty():
                resign = True
            else:
                current_state = pQueue.pop()
                explored.append(current_state)

                # print "Pop", count
                # current_state.print_info()
                # print

                if current_state.is_goal(goal):
                    found = True
                    final_state = current_state
                    #path = get_path(final_state)
                    #return path
                    #break
                else:
                    next_states = self.data_manager.get_next_states(current_state, goal)
                    for s in next_states:
                        if (prohibited_states is None or s not in prohibited_states) and (s not in explored) and (not pQueue.search(s)):
                            f = (s.arrived_time - start_time).total_seconds() + s.heuristic(goal) #f = g + h
                            pQueue.push(s, f)
                            # s.print_info()

                        # if (s not in explored) and (not pQueue.search(s)) :
                        #     f = (s.arrived_time - start_time).total_seconds() + s.heuristic(goal) #f = g + h
                        #     pQueue.push(s, f)


        path = None # list of states
        #processing result
        if found:
            path = get_path(final_state) 
            # print 'Total time: %s' %(final_state.arrived_time - start_time).total_seconds() 

        return path

    def shortest_duration_search(self, start_node, goal, k_shortest, start_time, end_time=None):

        # start = clock()

        start_time_list = self.data_manager.get_time_window(start_node, start_time)

        if len(start_time_list) == 0:
            return []

        # end = clock()
        # print "Finish find nearby location time list in %6.3f seconds" % (end - start)
        # print 'len of time list: ', len(start_time_list)
        # print 'time list: ', start_time_list

        # add default end_time
        # time must be between start_time and end of the day, if not specified
        if end_time == None:
            s_time = start_time_list[0]
            end_time = datetime.datetime(s_time.year, s_time.month, s_time.day, 23, 59, 59)

        results = []
        # durations_list = []
        for j, start_time in enumerate(start_time_list):
            start = clock()
            print '%d-th iterations' %(j)

            start_state = State(start_node, start_time, None, None)
            path = self.a_search(start_state, goal, start_time, None) # call a*
            if path != None:
                last_state = path[-1]
                if last_state.arrived_time > end_time:
                    break
                else:
                    # d = (last_state.arrived_time - start_time).seconds
                    # durations_list.append(d)
                    results.append(path)

            end = clock()
            print "Finish %d-th iterations in %6.3f seconds" % (j, end - start)

        #return only the the shortest duration
        # shortest_index = durations_list.index(min(durations_list))
        # return [results[shortest_index]]

        # return all results
        return results[:k_shortest]

#get path from start to goal
def get_path(final_state):
    path = []
    prv = final_state
    while prv.previous_state != None:
        path.append(prv)
        prv = prv.previous_state

    path.reverse()
    return Path(path) 

def get_path_cost(last_state, start_time):
    return (last_state.arrived_time - start_time).total_seconds()
