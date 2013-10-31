import MySQLdb
import data_structure
from constants import *
from data_structure import *
import datetime

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
		cur = self.query("SELECT id, name, longitude, latitude FROM `location`")
		all_nodes = []
		for row in cur.fetchall():
			#print row
			node = Node(row[0], row[1], row[3], row[2])
			all_nodes.append(node)
		cur.close()
		return all_nodes

	#get next bus steps from current state 
	#started_time of bus-steps get from DB, and always has to >= (arrived_time of current_step)
	def get_next_bus_steps(self, current_state):
		steps = []

		if current_state.node.id != START_NODE_ID:
			cursor = self.query("SELECT l.id, l.name, l.latitude, l.longitude, s.start_time, s.end_time FROM `location` l " + \
					             	  "JOIN `schedule` s ON l.id = s.end_loc_id WHERE s.start_loc_id = " + str(current_state.node.id))
			
			for row in cursor.fetchall(): 
				if row[4] > current_state.arrived_time:
					next_node = Node(row[0], row[1], row[2], row[3])
					step = Step(current_state.node, next_node, row[4], row[5], BUS_TYPE)
					steps.append(step)

			# print steps
		return steps

	#get walking_step from current state
	#started_time of walking-step is always = arrived_time of current_state
	def get_next_walking_steps(self, current_state):
		steps = []

		# get next nodes of starting node
		if current_state.node.id == START_NODE_ID: 
			all_nodes = self.get_all_node()
			for next_node in all_nodes:
				dist = util.distance(next_node.latitude, next_node.longitude, current_state.node.latitude, current_state.node.longitude)
				if dist <= MAX_DISTANCE:
					moving_time = util.get_moving_time(dist, WALKING_VELOCITY)
					step = Step(current_state.node, next_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, moving_time), WALKING_TYPE)
					steps.append(step)
		else:
			# get next nodes from a bus stop to other bus stops by walking
			cursor = self.query("SELECT l.id, l.name, l.latitude, l.longitude, d.time FROM `location` l " + \
					             	  "JOIN `distance` d ON l.id = d.end_loc_id WHERE d.start_loc_id = " + str(current_state.node.id))
			
			for row in cursor.fetchall(): 
				next_node = Node(row[0], row[1], row[2], row[3])
				moving_time = row[4]
				step = Step(current_state.node, next_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, moving_time), WALKING_TYPE)
				steps.append(step)


			# add step to goal_node
			distance = util.distance(current_state.node.latitude, current_state.node.longitude, current_state.goal_node.latitude, current_state.goal_node.longitude)
			to_goal_time = util.get_moving_time(distance, WALKING_VELOCITY)
			to_goal_step = Step(current_state.node, current_state.goal_node, current_state.arrived_time, util.add_secs(current_state.arrived_time, to_goal_time), WALKING_TYPE)
			steps.append(to_goal_step)

		return steps


	def close(self):
		self.db.close()


	


