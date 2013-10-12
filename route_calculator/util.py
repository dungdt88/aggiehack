import MySQLdb
import math
import heapq, random, sys
import gmap_api

MAX_DISTANCE = 2000
VELOCITY = 50 #km/h
WALKING_TYPE = "walking"
BUS_TYPE = "bus"
HOST = "localhost"
USERNAME = "root"
PASSWORD = "triplec"
DBNAME = "aggiehack"

# GOAL_NODE = Node()

from math import radians, cos, sin, asin, sqrt
def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km



class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.qset = set()

    def push(self, item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)
        self.qset.add(item.node.id)

    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
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
		self.longtitude = float(_long)

	def isEqual(self, checking_node):
		return abs(float(self.latitude) - float(checking_node.latitude)) < 0.001 and  \
			abs(float(self.longtitude) - float(checking_node.longtitude)) < 0.001


#Datastructure for step
class Step:
	def __init__(self, _start, _end, _start_time, _end_time, _type):
		self.start_node = _start
		self.end_node = _end
		self.start_time = _start_time
		self.end_time = _end_time
		self.type = _type


#calculate euclidean distance
# def distance(node1, node2):
# 	return math.sqrt((node1.latitude - node2.latitude) ** 2 + (node1.longtitude - node2.longtitude) ** 2)


#for test only
node11 = Node("node1", "node1", 10,10)
node44 = Node("node4", "node4", 40,40)
node22 = Node("node2", "node2", 20,20)
node33 = Node("node3", "node3", 30,30)

step12 = Step(node11, node22, 10, 11, "bus12")
step13 = Step(node11, node33, 10, 12, "bus13")
step24 = Step(node22, node44, 10, 13, "bus24")
step34 = Step(node22, node33, 11.5, 12.5, "bus44")


stepw12 = Step(node11, node22, 10, 11.5, "walk")
stepw23 = Step(node22, node33, 10, 15, "walk")
stepw24 = Step(node22, node44, 10, 18, "walk")
stepw34 = Step(node33, node44, 16, 19, "walk")


# #get available nodes
# def get_avai_nodes():
# 	return [node22, node33, node44]


#get next bus steps from current state from mySQL
#started_time of bus-steps get from DB, and always has to >= (arrived_time of current_step)
def get_next_bus_steps(current_state):
	# print 'bus start'
	sql_helper = SqlHelper(HOST, DBNAME, USERNAME, PASSWORD)
	available_nodes = sql_helper.get_node_around(current_state.node, "bus")
	steps = []

	#get schedule
	for node in available_nodes:
		cursor = sql_helper.query("SELECT * FROM `schedule` where start_loc_id = " + str(current_state.node.id) + " and end_loc_id = " + str(node.id))
		for row in cursor.fetchall(): #row = (startid, end id, start_time, end_time, routeID)
			print "compare time: %s, %f" %(row[2].split(' '), current_state.arrived_time)
			if row[2] > current_state.arrived_time:
				step = Step(current_state.node, node, row[2], row[3], row[4])
				steps.append(step)

	# print steps
	return steps


#get walking_step from current state
#from google API
#Note: started_time of walkinng-step is always = arrived-time of current_state
def get_walking_steps(current_state):
	#next_nodes = util.get_avai_nodes()
	#dist_list = dict()
	lat = current_state.node.latitude
	lng = current_state.node.longtitude

	available_nodes = []

	#select node from tbl_ current_state.end_node.id
	sql_helper = SqlHelper(HOST, DBNAME, USERNAME, PASSWORD)

	#get available nodes.
	#a available node must be within range and start from current node
	available_nodes = sql_helper.get_node_around(current_state.node)

	steps = []
	for node in available_nodes:
		walking_time = gmap_api.moving_time_gmap((float(lat), float(lng)), (float(node.latitude), float(node.longtitude)))
		step = Step(current_state.node, node, current_state.arrived_time, current_state.arrived_time + walking_time, WALKING_TYPE)
		steps.append(step)


	#add step to goal_node
	to_goal_time = gmap_api.moving_time_gmap((lat, lng), (current_state.goal_node.latitude, current_state.goal_node.longtitude))
	to_goal_step = Step(current_state.node, current_state.goal_node, current_state.arrived_time, current_state.arrived_time + to_goal_time, WALKING_TYPE)

	steps.append(to_goal_step)

	#close db
	sql_helper.close()

	return steps



##########################
class SqlHelper:
	def __init__(self, _host, _dbname, _username, _passwrd):
		self.db = MySQLdb.connect(_host, _username, _passwrd, _dbname)
		# self.host = _host
		# self.dbname = _dbname
		# self.username = _username
		# self.passwrd = _passwrd


	def query(self, _query):
		cursor = self.db.cursor()
		cursor.execute(_query)
		return cursor


	def get_all_node(self):
		cur = self.query("SELECT * FROM `location`")
		all_nodes = []
		for row in cur.fetchall():
			#print row
			node = Node(row[0], row[1], row[3], row[2])
			all_nodes.append(node)
		cur.close()
		return all_nodes


	def get_node_around(self, current_node, option=None):
		#print "culat=%f, culong=%f" %(current_node.latitude, current_node.longtitude)
		available_nodes = []		
		if current_node.id == -1: #aka: start node
			all_nodes = self.get_all_node()
			for node in all_nodes:
				#print "lat=%f, long=%f" %(node.latitude, node.longtitude)
				dist = gmap_api.distance_gmap(
					(float(node.latitude), float(node.longtitude)), (float(current_node.latitude), float(current_node.longtitude)))
				if dist <= MAX_DISTANCE:
					#print "find a node"
					available_nodes.append(node)
			return available_nodes

		cur = None

		if option == "bus":
			cur = self.query("SELECT * FROM `distance` WHERE start_loc_id = " + str(current_node.id))

		else: #request for walking distance
			cur = self.query("SELECT * FROM `distance` WHERE start_loc_id = " + str(current_node.id) + " and distance <= " + str(MAX_DISTANCE))

		for row in cur.fetchall():
			node_id2 = row[1]
			cur2 = self.query("SELECT * FROM `location` where id = " + str(node_id2))
			node2_info = cur2.fetchone()
			node = Node(node2_info[0], node2_info[1], node2_info[3], node2_info[2])
			available_nodes.append(node)
			cur2.close()

		cur.close()

		#all_nodes.append(GOAL_NODE)
		return available_nodes

	def close(self):
		self.db.close()


if __name__ == '__main__':
	testsql = SqlHelper(HOST, DBNAME, USERNAME, PASSWORD)
	testsql.get_all_node()

	#start_node = Node(-1, "start", 30.614, -96.339)
	#testsql.get_node_around(start_node, None)