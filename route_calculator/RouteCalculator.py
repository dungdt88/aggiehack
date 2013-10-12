#Anh Nguyen
import util #util file


#state at current position
#contain information for making decision how to go next
class State:
	def __init__(self, _node, _started_time=0, _arrived_time=0, _how_I_got_here=None, _prev_state=None):
		self.node = _node
		self.started_time = _started_time
		self.arrived_time = _arrived_time
		self.previous_step = _how_I_got_here #the step that take you here
		self.previous_state = _prev_state

	#Return time to get from current State to next State
	def get_time(self, to_state, step):
		return 0

	#Heuristic function
	#Euclidean distance
	def heuristic(self, goal_state):
		return float(util.distance(self.node, goal_state.node) / util.VELOCITY)
		#return util.distance(self.node, goal_state.node)


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
		next_states = [] #util.PriorityQueue()

		for step in next_steps:
			new_started_time = self.arrived_time
			new_arrived_time = new_started_time + (step.end_time - step.start_time)
			new_node = step.end_node
			new_state = State(new_node, new_started_time, new_arrived_time, step, self)
			next_states.append(new_state) #push(new_state, (new_arrived_time - new_started_time)) #push to priority queue

		return next_states

	def print_info(self):
		if self.previous_step == None:
			print 'Name= %s, start_time= %f, arrived_time= %f' %(self.node.name, self.started_time, self.arrived_time)
		else:
			print 'Name= %s, start_time= %f, arrived_time= %f, type=%s' %(self.node.name, self.started_time, self.arrived_time, self.previous_step.type)



class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start = _from
        self.destination = _to
        self.start_time = _start_time

        #self.start_state = State(self.start, _start_time, _start_time, None, None)
        #self.goal_state = State(self.destination, -1, -1, None, None)


    #check if a state is the goal state
    def is_goal(self, test_state, goal_state):
    	return goal_state.isEqual(test_state.node)

    
    #get path from start to goal
    def get_path(self, final_state):
    	prv = final_state
    	path = []
    	while prv.previous_step != None:
    		path.append(prv.previous_step)
    	return path.reverse()


    def a_super_star(self, start_state, goal_state):
    	found = False
    	resign = False
    	pQueue = util.PriorityQueue()
    	pQueue.push(start_state, 0)
    	explored = []
    	final_state = None

    	while not found and not resign:
    		if pQueue.isEmpty():
    			print '### Search terminated without sucess'
    		else:
    			current_state = pQueue.pop()
    			explored.append(current_state.node.ids)
    			if self.is_goal(current_state, goal_state):
    				found = True
    				final_state = current_state
    				print '### Search terminated without sucess'
    			else:
    				next_states = current_state.gen_next_state()
    				for s in next_states:
    					#tmp_compare = (s.node.id, s.previous_step.type)
    					if (s.node.id not in explored):
    						f = (s.arrived_time - start_state.started_time) + s.heuristic(goal_state) #f = g + h
    						pQueue.push(s, f)

		path = None
    	#processing result
    	if found:
    		path = self.get_path(final_state)

    	return path

def test():
	node1 = util.node11
	state1 = State(node1, 10, 10, None, None)

	#state1.print_info()

	next_states = state1.gen_next_state()
	for s in next_states:
		s.print_info()

if __name__ == '__main__':
	test()