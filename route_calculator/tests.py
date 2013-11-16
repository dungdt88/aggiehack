import RouteCalculator
from constants import *
from data_structure import *
from db_util import *
from RouteCalculator import *
from time import clock

if __name__ == '__main__':

	# for test_node in testsql.get_all_node():
	# 	print test_node.id, test_node.name, test_node.latitude, test_node.longitude

	goal_node_1 = Node(-1, "End at MSC", 30.612771,-96.342081) 
	goal_node_2 = Node(-1, "End at Wisenbaker", 30.62095300, -96.33822100)

	start_node_1 = Node(-1, "Start at Applebee's", 30.629807,-96.337523) 
	start_node_2 = Node(-1, "Start at Home", 30.638226, -96.32246)
	start_node_3 = Node(-1, "Start at Aggie Station", 30.624064,-96.354003)

	start_time = datetime.datetime(2013, 11, 10, 10, 5, 0, 0)

	start = clock();
	calculator = RouteCalculator(start_node_1, goal_node_2, start_time)
	end = clock();
	print "Finish initialization in %6.3f seconds" % (end - start)

	# print "From Applebee's to Wisenbaker"
	# start = clock();
	# path = calculator.a_search()
	# end = clock();
	# print "Finish searching in %6.3f seconds" % (end - start)
	# print path

	# print "From Home to MSC"
	# start = clock();
	# calculator = RouteCalculator(start_node_2, goal_node_1, start_time)
	# path = calculator.a_search()
	# end = clock();
	# print "Finish searching in %6.3f seconds" % (end - start)	
	# print path

	print "From Aggie Station to MSC"
	start = clock();
	calculator = RouteCalculator(start_node_3, goal_node_1, start_time)
	path = calculator.a_search()
	end = clock();
	print "Finish searching in %6.3f seconds" % (end - start)	
	print path
