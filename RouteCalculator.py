#Anh Nguyen
import util #util file


#state at current position
#contain information for making decision how to go next
class State:
	def __init__(self, _node, _started_time=0, _arrived_time=0, _how_I_got_here=None, _prev_state=None):
		self.previous_state = _prev_state
		self.node = _node
		self.started_time = _started_time
		self.arrived_time = _arrived_time
		self.previous_step = _how_I_got_here #the step that take you here


	#Return time to get from current State to next State
	def get_time(self, to_state, step):
		return 0


	#Heuristic function
	#Euclidean distance
	def heuristic(self, goal_state):
		return util.distance(self.node, goal_state.node)


	#Return all possible steps from current state
	def get_steps_from_current_state(self):
		#query mysql, table "schedule" for node.nodeID
		#mysql return all fixed "bus-step" that can be processed.
		bus_steps = util.get_next_bus_steps(self)
		#also query google map for walking-step
		walking_steps = util.get_walking_steps(self)

		return (bus_steps + walking_steps)


	#Generate possible states by consider possible ways to get from 1 States to available nodes around
	def gen_next_state(self):
		# next_nodes = util.get_avai_nodes()
		# dist_list = dict()
		# for n in next_nodes:
		# 	d = util.distance(n, self.node)
		# 	dist_list[str(d)] = n

		# #[(distance, node), ...]
		# sorted_dist = sorted(dist_list.items(), key=lambda t: t[0])

		# #get the nearest state in term of time cost
		next_steps = self.get_steps_from_current_state()
		next_states = util.PriorityQueue()

		for step in next_steps:
			new_started_time = self.arrived_time
			new_arrived_time = new_started_time + (step.end_time - step.start_time)
			new_node = step.end_node
			new_state = State(new_node, new_started_time, new_arrived_time, step, self)
			
			next_states.push(new_state, (new_arrived_time - new_started_time)) #push to priority queue

		#gen next states
		# for item in sorted_dist:
		# 	new_state = State(item[1], self.arrived_time, self.get_time(item[1]), self.previous_step, self)
		# 	next_states.append(new_state)

		return next_states

	def print_info(self):
		print 'Name= %s, start_time= %f, arrived_time= %f' %(self.node.name, self.started_time, self.arrived_time)


class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start = _from
        self.destination = _to
        self.start_time = _start_time

        #self.start_state = State(self.start, _start_time, _start_time, None, None)
        #self.goal_state = State(self.destination, -1, -1, None, None)


    def is_goal(self, test_state, goal_state):
    	return goal_state.isEqual(test_state.node)

    def check_expanded(self, test_state):
    	pass

    def a_super_star(self, start_state, goal_state):
    	
    	pass



def test():
	node1 = util.Node("node1", "node1", 1,1)
	state1 = State(node1, 10, 10, None, None)
	state1.print_info()

	next_states = state1.gen_next_state()
	shortest = next_states.pop()
	shortest.print_info()

if __name__ == '__main__':
	test()