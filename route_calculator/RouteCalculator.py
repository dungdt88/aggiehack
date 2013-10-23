#Anh Nguyen
import util #util file
import json, sys, random
import simplejson


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
	# 	return 0

	#Heuristic function
	#Euclidean distance
	def heuristic(self):
		return float(util.distance(self.node.longtitude, self.node.latitude , self.goal_node.longtitude, self.goal_node.latitude) / util.VELOCITY)*3600
		#return util.distance(self.node, goal_state.node)


	#Return all possible steps from current state
	def get_steps_from_current_state(self):
		#2 steps:
		#step 1: query mysql, table "schedule" for node.nodeID
		#mysql return all fixed "bus-step" that can be processed.
		bus_steps = util.get_next_bus_steps(self)

		#step2: also query google map for walking-step
		walking_steps = util.get_walking_steps(self)

		return (bus_steps + walking_steps)


	#check if current_state is goal
	def is_goal(self):
		return self.node.isEqual(self.goal_node)


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
			new_started_time = step.start_time
			new_arrived_time = new_started_time + (step.end_time - step.start_time)
			new_node = step.end_node
			new_state = State(new_node, self.goal_node, new_started_time, new_arrived_time, step, self)
			next_states.append(new_state) #push(new_state, (new_arrived_time - new_started_time)) #push to priority queue

		return next_states

	def print_info(self):
		if self.previous_step == None:
			print 'Name= %s, start_time= %f, arrived_time= %f' %(self.node.name, self.started_time, self.arrived_time)
		else:
			print 'Name= %s, start_time= %f, arrived_time= %f, type=%s' %(self.node.name, self.started_time, self.arrived_time, self.previous_step.type)



class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start_node = _from
        self.goal_node = _to
        self.start_time = _start_time * 3600

        #self.start_state = State(self.start, _start_time, _start_time, None, None)
        #self.goal_state = State(self.destination, -1, -1, None, None)


    # #check if a state is the goal node
    # def is_goal(self, test_state, goal_node):
    # 	return goal_node.isEqual(test_state.node)


    #get path from start to goal
    def get_path(self, final_state):
    	prv = final_state
    	path = []
    	while prv.previous_state != None:
            path.append(prv.previous_step)
            prv = prv.previous_state

        # print path[0].type
        path.reverse()

        # newarray = dict()
        string = ""
        for i, p in enumerate(path):
            

            f = p.start_node.name
            t = p.end_node.name
            time1 = p.start_time
            ty = p.type
            # tmp = dict()
            # tmp['from'] = f
            # tmp['to'] = t
            # tmp['time'] = time1
            # tmp['type'] = ty
            
            string += f + ','+t+','+str(time1)+','+ty+"\n"

            # newarray[i] = tmp

    	return string


    def get_parents(self, state):
        prv = state
        path = []
        path.append(prv)
        while prv.previous_state != None:
            path.append(prv.previous_state)
            prv = prv.previous_state

        path.reverse()

        # for p in path:
        #     print p.node.name

        return path


    def a_search(self):
        # print 'start a*'

    	found = False
    	resign = False
    	pQueue = util.PriorityQueue()

    	start_state = State(self.start_node, self.goal_node, self.start_time, self.start_time, None, None)

        # print 'start state'
        # start_state.print_info()

    	pQueue.push(start_state, 0)
    	explored = []
    	final_state = None

    	while not found and not resign:
    		if pQueue.isEmpty():
    			resign = True
    			#print '### Search terminated without sucess'
    		else:
    			current_state = pQueue.pop()
                # print 'current state'
                # current_state.print_info()
                # current_state.print_info()
                explored.append(current_state.node.id)
                if current_state.is_goal():

                	found = True
                	final_state = current_state
                	# print '### Search terminated with sucess'
                        path = self.get_path(final_state)
                        return path
                else:
                	next_states = current_state.gen_next_state()
                	for s in next_states:
                            #s.print_info()
                            # print 'path'
                            # self.get_parents(s)
                            if (s.node.id not in explored and pQueue.search(s.node) == False):
                                f = (s.arrived_time - start_state.started_time) + s.heuristic() #f = g + h
                                pQueue.push(s, f)

		path = None
    	#processing result
    	if found:
    		path = self.get_path(final_state)

    	return path

def main(lat1, long1, lat2, long2, start_time):

	start_node = util.Node(-1, "start", long1, lat1)
	goal_node = util.Node(-2, "goal", long2, lat2)

	calculator = RouteCalculator(start_node, goal_node, start_time)
        path = calculator.a_search()


	print path


def default(str):
    return str + ' [Default: %default]'

def readCommand(argv):
    from optparse import OptionParser
    usageStr = """
    USAGE:      python RouteCalculator.py <options>
    EXAMPLES:   (1) python RouteCalculator.py -a 5 -b 3 -c 1 -d 2 -s 10
    """
    parser = OptionParser(usageStr)
    parser.add_option('-a', '--lata', dest='lata', type='float',
        help=default('d'), metavar='LATA', default=0)
    parser.add_option('-b', '--longa', dest='longa', type='float',
        help=default('d'), metavar='LONGA', default=0)
    parser.add_option('-c', '--latb', dest='latb', type='float',
        help=default('d'), metavar='LATB', default=0)
    parser.add_option('-d', '--longb', dest='longb', type='float',
        help=default('d'), metavar='LONGB', default=0)
    parser.add_option('-s', '--start', dest='start', type='float',
        help=default('d'), metavar='START', default=0)

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    #parser is incomplete - further enhancement required
    return options

if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    main(args.lata, args.longa, args.latb, args.longb, args.start)


# def


# def test():
# 	node1 = util.node11
# 	state1 = State(node1, 10, 10, None, None)

# 	#state1.print_info()

# 	next_states = state1.gen_next_state(util.node44)
# 	for s in next_states:
# 		s.print_info()

# if __name__ == '__main__':
# 	test()
