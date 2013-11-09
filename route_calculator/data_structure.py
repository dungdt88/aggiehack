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
        self.qset.add(item.end_node.id)

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


# #Datastructure for step
# class Step:
# 	def __init__(self, _start, _end, _start_time, _end_time, _type):
# 		self.start_node = _start
# 		self.end_node = _end
# 		self.start_time = _start_time
# 		self.end_time = _end_time
# 		self.type = _type

class WalkingTime:
  def __init__(self, _start, _end, _time):
        self.start_loc_id = _start
        self.end_loc_id = _end
        self.time = _time

#state at current position
#contain information for making decision how to go next
class Step:
    def __init__(self, _start_node, _end_node, _start_time=0, _end_time=0, _trans_type="", _previous_step=None):
        self.start_node = _start_node
        self.end_node = _end_node
        self.start_time = _start_time
        self.end_time = _end_time
        self.trans_type = _trans_type
        self.previous_step = _previous_step

    #Heuristic function
    #Euclidean distance
    def heuristic(self, goal_node):
        return util.get_moving_time(util.distance(self.end_node.latitude, self.end_node.longitude, goal_node.latitude, goal_node.longitude), BUS_VELOCITY)


    #check if current_state is goal
    def is_goal(self, goal_node):
        return self.end_node.isEqual(goal_node)


    def print_info(self):
        print 'Start node= %s, end node=%s, start_time= %f, end_time= %f' %(self.start_node.name, self.end_node, self.start_time, self.end_time)



