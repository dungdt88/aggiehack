import RouteCalculator
from constants import *
from data_structure import *
from data_manager import *
from RouteCalculator import *
from time import clock


def convert_results_to_json(path_list):
    results_list = []
    for path in path_list:
        steps = []
        for i, state in enumerate(path):
            if state.previous_step != None:
                p  = state.previous_step
                start = {'name': p.start_node.name, 'long': str(p.start_node.longitude), 'lat': str(p.start_node.latitude)}
                end = {'name': p.end_node.name, 'long': str(p.end_node.longitude), 'lat': str(p.end_node.latitude)}
                start_time = p.start_time
                duration = (p.end_time - p.start_time).seconds
                typn = p.type
                bus_number = ""
                if typn is not WALKING_TYPE:
                    bus_number = typn
                    typn = BUS_TYPE
                one_step = {'start': start, 'end':end, 'type':typn, 'bus_number': bus_number, 'duration': duration, "start_time": start_time}

                steps.append(one_step)

        results_list.append(steps)
    return results_list


if __name__ == '__main__':

	K_SHORTEST = 5

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

	#print "From Home to MSC"
	start = clock();
	start_state = State(start_node_2, start_time, None, None)
	path_list = calculator.search(start_state, goal_node_1, start_time, K_SHORTEST)
	end = clock();
	print "Finish searching in %6.3f seconds" % (end - start)	
	#print "Found", len(path_list)
	
	print convert_results_to_json(path_list)

	# print "From Aggie Station to MSC"
	# start = clock();
	# start_state = State(start_node_3, start_time, None, None)
	# path_list = calculator.search(start_state, goal_node_1, start_time, K_SHORTEST)
	# end = clock();
	# print "Finish searching in %6.3f seconds" % (end - start)	
	# print "Found", len(path_list)
	# for p in path_list:
	# 	p.print_info()


