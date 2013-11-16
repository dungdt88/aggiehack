import util 
import data_structure
import data_manager
import json, sys, random
from data_manager import *
from data_structure import *

class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start_node = _from
        self.goal_node = _to
        self.start_time = _start_time
        self.data_manager = DataManager()

    def a_search(self):
        found = False
        resign = False
        pQueue = PriorityQueue()

        start_state = State(self.start_node, self.start_time, None, None)
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
                explored.append(current_state.node.id)

                print "Pop", count
                current_state.print_info()

                if current_state.is_goal(self.goal_node):
                    found = True
                    final_state = current_state
                    path = get_path(final_state)
                    return path
                else:
                    next_states = self.data_manager.get_next_states(current_state, self.goal_node)
                    for s in next_states:
                        f = (s.arrived_time - self.start_time).total_seconds() + s.heuristic(self.goal_node) #f = g + h
                        pQueue.push(s, f)

                        # if (s.node.id not in explored and pQueue.search(s.node) == False):
                        #     f = (s.arrived_time - self.start_time).total_seconds() + s.heuristic(self.goal_node) #f = g + h
                        #     pQueue.push(s, f)


        path = None
        #processing result
        if found:
            path = get_path(final_state)
            # print 'Total time: %s' %(final_state.arrived_time - self.start_time).total_seconds() 

        print "Queue length: ", pQueue.length(), "; Iteration: ", count

        return path
        