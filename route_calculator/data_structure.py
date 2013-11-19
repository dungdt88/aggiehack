import constants
from constants import *
import util
import heapq, random, sys

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        # self.qset = set()

    def __len__(self):
        return len(self.heap)

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.heap, pair)
        # self.qset.add(item)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def search(self, obj):
        for item in self.heap:
            if obj == item[1]:
                return True
        return False

    def isEmpty(self):
        return len(self.heap) == 0


class Path:
    def __init__(self, _state_list):
        self.state_list = _state_list

    def __eq__(self, other):
        if len(self.state_list) != len(other.state_list):
            return False
        else:
            for i in range(len(self.state_list)):
                if not self.state_list[i] == other.state_list[i]:
                    #self.state_list[i].print_info()
                    #other.state_list[i].print_info()
                    return False
            return True

    def __getitem__(self, index):
        return self.state_list[index]

    def __len__(self):
        return len(self.state_list)

    def get_last(self):
        return self.state_list[len(self.state_list)-1]

    def print_info(self):
        # path = []
        string = ""
        for s in self.state_list:
            if s.previous_step != None:
                p = s.previous_step
                s = p.start_node.name
                e = p.end_node.name
                st = p.start_time
                et = p.end_time
                type = p.type
                
                string += s + ', ' + e + ', ' + str(st) + ', ' + str(et) + ', ' + type + "\n"
        print "Path:\n", string    

#Datastructure for node
class Node:
    def __init__(self, _id, _name, _lat, _long):
        self.id = _id
        self.name = _name
        self.latitude = float(_lat)
        self.longitude = float(_long)

    def __eq__(self, other):
        return self.id == other.id

    def is_close_by_in_threshold(self, checking_node):
        return abs(float(self.latitude) - float(checking_node.latitude)) < 0.0001 and  abs(float(self.longitude) - float(checking_node.longitude)) < 0.0001

    def print_info(self):
        print 'id=%s, name=%s, lat=%f, long=%f' % (self.id, self.name, self.latitude, self.longitude)

#Datastructure for step
class Step:
    def __init__(self, _start, _end, _start_time, _end_time, _type):
        self.start_node = _start
        self.end_node = _end
        self.start_time = _start_time
        self.end_time = _end_time
        self.type = _type

    def __eq__(self, other):
        return self.start_node == other.start_node and \
               self.end_node == other.end_node and \
               self.start_time == other.start_time and \
               self.end_time == other.end_time and \
               self.type == other.type       

    def print_info(self):
        print 'Start node=%s %s, end node=%s %s, start_time=%s, end_time=%s, by=%s' \
            %(self.start_node.id, self.start_node.name, self.end_node.id, self.end_node.name, self.start_time, self.end_time, self.type)

#state at current position
#contain information for making decision how to go next
class State:
    def __init__(self, _node, _arrived_time=0, _how_I_got_here=None, _prev_state=None):
        self.node = _node
        # self.started_time = _started_time       # time leaving previous node
        self.arrived_time = _arrived_time       # time arrived at this node
        self.previous_step = _how_I_got_here    # the step that take you here
        self.previous_state = _prev_state       # previous state to allow back tracking and get final path

    def __eq__(self, other):
        return self.node == other.node and \
               self.arrived_time == other.arrived_time and \
               ((self.previous_step is None and other.previous_step is None) or 
                    (self.previous_step is not None and other.previous_step is not None and self.previous_step == other.previous_step))

    #Heuristic function based on Euclidean distance
    def heuristic(self, goal_node):
        return util.get_moving_time(util.distance(self.node.latitude, self.node.longitude , goal_node.latitude, goal_node.longitude), BUS_VELOCITY)

    #check if current_state is goal
    def is_goal(self, goal_node):
        return self.node.is_close_by_in_threshold(goal_node)


    def print_info(self):
        if self.previous_step is None:
            print 'Name= %s, arrived_time= %s' %(self.node.name, self.arrived_time)
        else:
            print 'Name= %s, arrived_time= %s, previous=%s, type=%s' %(self.node.name, self.arrived_time, self.previous_step.start_node.name, self.previous_step.type)

class WalkingTime:
    def __init__(self, _start, _end, _time):
        self.start_loc_id = _start
        self.end_loc_id = _end
        self.time = _time
