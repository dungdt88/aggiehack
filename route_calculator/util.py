import MySQLdb
import math
import heapq, random, sys

MAX_DISTANCE = 1000
VELOCITY = 40 #miles/h

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        #self.qset = ()

    def push(self, item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)
        #self.qset.add(item.node.id)

    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
        return item

    # def search(self, node):
    #     if node.id not in self.qset:
    #         return False
    #     return True

    def isEmpty(self):
        return len(self.heap) == 0


#Datastructure for node
class Node:
	def __init__(self, _id, _name, _lat, _long):
		self.id = _id
		self.name = _name
		self.latitude = _lat
		self.longtitude = _long

	def isEqual(self, checking_node):
		return abs(self.latitude - checking_node.latitude) < 0.01 and  abs(self.longtitude - checking_node.longtitude) < 0.01


#Datastructure for step
class Step:
	def __init__(self, _start, _end, _start_time, _end_time, _type):
		self.start_node = _start
		self.end_node = _end
		self.start_time = _start_time
		self.end_time = _end_time
		self.type = _type


#calculate euclidean distance
def distance(node1, node2):
	return math.sqrt((node1.latitude - node2.latitude) ** 2 + (node1.longtitude - node2.longtitude) ** 2)



#for test only
node11 = Node("node1", "node1", 10,10)
node22 = Node("node2", "node2", 20,20)
node33 = Node("node3", "node3", 30,30)
node44 = Node("node4", "node4", 40,40)

step12 = Step(node11, node22, 10, 11, "bus12")
step13 = Step(node11, node33, 10, 12, "bus13")
step24 = Step(node22, node44, 10, 13, "bus24")
step34 = Step(node22, node33, 11.5, 12.5, "bus44")


stepw12 = Step(node11, node22, 10, 11.5, "walk")
stepw23 = Step(node22, node33, 10, 15, "walk")
stepw24 = Step(node22, node44, 10, 18, "walk")
stepw34 = Step(node33, node44, 16, 19, "walk")


#get available nodes
def get_avai_nodes():
	return [node22, node33, node44]


#get next bus steps from current state from mySQL
#started_time of bus-steps get from DB, and always has to >= (arrived_time of current_step + walking time from current to bus)
def get_next_bus_steps(current_state):
	steps = [step12, step13]
	return steps


#get walking_step from current state
#from google API
#Note: started_time of walkinng-step is always = arrived-time of current_state
def get_walking_steps(current_state):
	#next_nodes = util.get_avai_nodes()
	#dist_list = dict()
	steps = [stepw12]
	return steps


##########################
class SqlHelper:
	def __init__(self, _host, _dbname, _username, _passwrd):
		self.db = MySQLdb(_host, _username, _passwrd, _dbname)
		# self.host = _host
		# self.dbname = _dbname
		# self.username = _username
		# self.passwrd = _passwrd


	def query(self, _query):
		cursor = self.db.cursor()
		cursor.execute(_query)


	def close(self):
		self.db.close()
