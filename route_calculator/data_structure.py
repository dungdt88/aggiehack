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


#Datastructure for node
class Node:
	def __init__(self, _id, _name, _lat, _long):
		self.id = _id
		self.name = _name
		self.latitude = float(_lat)
		self.longitude = float(_long)

	def isEqual(self, checking_node):
		return abs(float(self.latitude) - float(checking_node.latitude)) < 0.001 and  \
			abs(float(self.longitude) - float(checking_node.longitude)) < 0.001


#Datastructure for step
class Step:
	def __init__(self, _start, _end, _start_time, _end_time, _type):
		self.start_node = _start
		self.end_node = _end
		self.start_time = _start_time
		self.end_time = _end_time
		self.type = _type

#state at current position
#contain information for making decision how to go next
class State:
    def __init__(self, _node, _goal_node, _started_time=0, _arrived_time=0, _how_I_got_here=None, _prev_state=None):
        self.node = _node
        self.goal_node = _goal_node
        self.started_time = _started_time
        self.arrived_time = _arrived_time
        self.previous_step = _how_I_got_here #the step that take you here
        self.previous_state = _prev_state

    # #Return time to get from current State to next State
    # def get_time(self, to_state, step):
    #   return 0

    #Heuristic function
    #Euclidean distance
    def heuristic(self):
        return util.get_moving_time(util.distance(self.node.latitude, self.node.longitude , self.goal_node.latitude, self.goal_node.longitude), BUS_VELOCITY)


    #check if current_state is goal
    def is_goal(self):
        return self.node.isEqual(self.goal_node)


    def print_info(self):
        if self.previous_step == None:
            print 'Name= %s, start_time= %f, arrived_time= %f' %(self.node.name, self.started_time, self.arrived_time)
        else:
            print 'Name= %s, start_time= %f, arrived_time= %f, type=%s' %(self.node.name, self.started_time, self.arrived_time, self.previous_step.type)



