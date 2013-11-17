import RouteCalculator
from constants import *
from data_structure import *
from data_manager import *
from RouteCalculator import *
from time import clock

if __name__ == '__main__':

	K_SHORTEST = 3

	# for test_node in testsql.get_all_node():
	# 	print test_node.id, test_node.name, test_node.latitude, test_node.longitude

	goal_node_1 = Node(-1, "End at MSC", 30.612771,-96.342081) 
	goal_node_2 = Node(-1, "End at Wisenbaker", 30.62095300, -96.33822100)

	start_node_1 = Node(-1, "Start at Applebee's", 30.629807,-96.337523) 
	start_node_2 = Node(-1, "Start at Home", 30.638226, -96.32246)
	start_node_3 = Node(-1, "Start at Aggie Station", 30.624064,-96.354003)

	start_time = datetime.datetime(2013, 11, 10, 10, 30, 0, 0)

	start = clock();
	calculator = RouteCalculator()
	end = clock();
	print "Finish initialization in %6.3f seconds" % (end - start)

	# print "From Applebee's to Wisenbaker"
	# start = clock();
	# start_state = State(start_node_1, start_time, None, None)
	# path_list = calculator.search(start_state, goal_node_2, start_time, K_SHORTEST)
	# end = clock();
	# print "Finish searching in %6.3f seconds" % (end - start)

	print "From Home to MSC"
	start = clock();
	start_state = State(start_node_2, start_time, None, None)
	path_list = calculator.search(start_state, goal_node_1, start_time, K_SHORTEST)
	end = clock();
	print "Finish searching in %6.3f seconds" % (end - start)	
	print "Found", len(path_list)
	for p in path_list:
		p.print_info()

	# print "From Aggie Station to MSC"
	# start = clock();
	# start_state = State(start_node_3, start_time, None, None)
	# path_list = calculator.search(start_state, goal_node_1, start_time, K_SHORTEST)
	# end = clock();
	# print "Finish searching in %6.3f seconds" % (end - start)	
	# print "Found", len(path_list)
	# for p in path_list:
	# 	p.print_info()
