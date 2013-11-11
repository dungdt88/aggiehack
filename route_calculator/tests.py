import RouteCalculator
from constants import *
from data_structure import *
from db_util import *
from RouteCalculator import *
from time import clock

if __name__ == '__main__':

	# for test_node in testsql.get_all_node():
	# 	print test_node.id, test_node.name, test_node.latitude, test_node.longitude

	start_node = Node(1, "MSC", 30.61393756, -96.33965217) 
	goal_node = Node(2, "Wisenbaker", 30.62095300, -96.33822100)
	my_node = Node(-1, "ETB", 30.630231, -96.338425) #ETB
	home_node = Node(-1, "home", 30.638226, -96.32246)
	start_time = datetime.datetime(2013, 10, 12, 8, 0, 0, 0)


	# current_state = State(start_node, goal_node, datetime.datetime.now(), start_time)

	# next_bus_steps = testsql.get_next_bus_steps(current_state)
	# for step in next_bus_steps:
	# 	print step.start_node.id, step.end_node.id, step.start_time, step.end_time, step.type
	# print len(next_bus_steps)

	# next_steps = get_next_steps(current_state)
	# for step in next_steps:
	# 	print step.start_node.id, step.end_node.id, step.start_time, step.end_time, step.type
	# print len(next_steps)

	# my_node = Node(-1, "my node", 30.630231,dd -96.338425)
	# current_state = State(my_node, goal_node, datetime.datetime.now(), start_time)
	# next_walking_steps = testsql.get_next_walking_steps(current_state)
	# for step in next_walking_steps:
	# 	print step.start_node.id, step.end_node.id, step.start_time, step.end_time, step.type
	# print len(next_walking_steps)

	start = clock();
	calculator = RouteCalculator(my_node, goal_node, start_time)
	end = clock();
	print "Finish initialization in %6.3f seconds" % (end - start)

	print "from ETB to Wisenbaker"
	start = clock();
	path = calculator.a_search()
	end = clock();
	print "Finish searching in %6.3f seconds" % (end - start)
	print path

	print "from Home to MSC"
	start = clock();
	calculator = RouteCalculator(home_node, start_node, start_time)
	path = calculator.a_search()
	end = clock();
	print "Finish searching in %6.3f seconds" % (end - start)	
	print path
