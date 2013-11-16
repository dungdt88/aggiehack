import constants
from constants import *
import util
import heapq, random, sys

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.qset = set()

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.heap, pair)
        self.qset.add(item.node.id)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def search(self, node):
        if node.id not in self.qset:
            return False
        return True

    def isEmpty(self):
        return len(self.heap) == 0

    def length(self):
        return len(self.heap)


#Datastructure for node
class Node:
    def __init__(self, _id, _name, _lat, _long):
        self.id = _id
        self.name = _name
        self.latitude = float(_lat)
        self.longitude = float(_long)

    def __eq__(self, other):
        return self.id == other.id

    def isEqual(self, checking_node):
        return abs(float(self.latitude) - float(checking_node.latitude)) < 0.0001 and  abs(float(self.longitude) - float(checking_node.longitude)) < 0.0001

#Datastructure for step
class Step:
    def __init__(self, _start, _end, _start_time, _end_time, _type):
        self.start_node = _start
        self.end_node = _end
        self.start_time = _start_time
        self.end_time = _end_time
        self.type = _type

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

    #Heuristic function based on Euclidean distance
    def heuristic(self, goal_node):
        return util.get_moving_time(util.distance(self.node.latitude, self.node.longitude , goal_node.latitude, goal_node.longitude), BUS_VELOCITY)

    #check if current_state is goal
    def is_goal(self, goal_node):
        return self.node.isEqual(goal_node)


    def print_info(self):
        if self.previous_step == None:
            print 'Name= %s, arrived_time= %s' %(self.node.name, self.arrived_time)
        else:
            print 'Name= %s, arrived_time= %s, previous=%s, type=%s' %(self.node.name, self.arrived_time, self.previous_step.start_node.name, self.previous_step.type)

class WalkingTime:
    def __init__(self, _start, _end, _time):
        self.start_loc_id = _start
        self.end_loc_id = _end
        self.time = _time
