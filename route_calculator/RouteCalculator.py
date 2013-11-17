import util 
import data_structure
import data_manager
import json, sys, random
from data_manager import *
from data_structure import *

class RouteCalculator:

    def __init__(self):
        self.data_manager = DataManager()

    def search(self, start_node, goal, start_time, k_shortest):
        path_list = [] # each list consists of path, which is a list of states
        path_found = self.a_search(start_node, goal, start_time)
        # path_found.print_info()
        path_list.append(path_found)

        potential_path_list = PriorityQueue()
        
        for k in range(1, k_shortest+1): #from 1 to k
            
            if len(path_list) >= k:
                #remove each state of the final path from the graph
                for spur_node in path_list[k-1]:
                    print "Spur"
                    spur_node.print_info()
                    prohibited_states = []
                    prohibited_states.append(spur_node)
                    print "prohibited length", len(prohibited_states)
                    
                    alternate_path = self.a_search(start_node, goal, start_time, prohibited_states)

                    if potential_path_list.search(alternate_path) == False and alternate_path not in path_list:
                        print "Alternate"
                        alternate_path.print_info()
                        path_cost = get_path_cost(alternate_path.get_last(), start_time)
                        potential_path_list.push(alternate_path, path_cost)

                if not potential_path_list.isEmpty(): 
                    path_found = potential_path_list.pop()
                    # path_found.print_info()
                    path_list.append(path_found)
            
        return path_list

    def a_search(self, start_node, goal, start_time, prohibited_states=[]):
        found = False
        resign = False
        pQueue = PriorityQueue()

        pQueue.push(start_node, 0)
        explored = []
        final_state = None

        count = 0
        while not found and not resign:
            count = count + 1

            if pQueue.isEmpty():
                resign = True
            else:
                current_state = pQueue.pop()
                # explored.append(current_state.node.id)
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
                        if prohibited_states is None or s not in prohibited_states:
                            f = (s.arrived_time - start_time).total_seconds() + s.heuristic(goal) #f = g + h
                            pQueue.push(s, f)
                            # s.print_info()

                        # if (s.node.id not in explored and pQueue.search(s.node) == False):
                        #     f = (s.arrived_time - start_time).total_seconds() + s.heuristic(goal) #f = g + h
                        #     pQueue.push(s, f)


        path = None # list of states
        #processing result
        if found:
            path = get_path(final_state) 
            # print 'Total time: %s' %(final_state.arrived_time - start_time).total_seconds() 

        # print "Queue length: ", pQueue.length(), "; Iteration: ", count

        return path

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