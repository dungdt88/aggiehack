import util 
import data_structure
import data_manager
import json, sys, random
from data_structure import *
from data_manager import *
from time import clock

class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start_node = _from
        self.goal_node = _to
        self.start_time = _start_time
        self.data_manager = DataManager()

    def a_search(self):
    	found = False
    	resign = False
    	pQueue = PriorityQueue()

    	start_step = Step(self.start_node, self.start_node, self.start_time, self.start_time)
    	pQueue.push(start_step, 0)
    	explored = []
    	final_step = None

        count = 100
    	while not found and not resign and count > 0:
            count = count - 1
            if pQueue.isEmpty():
                resign = True
            else:
                current_step = pQueue.pop()
                explored.append(current_step)
                print "Pop"
                current_step.print_info() 

                if current_step.is_goal(self.goal_node):
                    found = True
                    final_step = current_step
                    path = get_path(final_step)
                    return path
                else:
                    next_steps_and_durations = self.data_manager.get_next_steps_and_durations(current_step, self.goal_node) #(next_steps, total_time)
                    for s, t in next_steps_and_durations:
                        if (s not in explored and pQueue.search(s) == False):
                            f = (s.end_time - start_step.start_time).total_seconds() + s.heuristic(self.goal_node) #f = g + h
                            pQueue.push(s, f)
                            # s.print_info()
                            # print "Total time so far", (s.end_time - start_step.start_time).total_seconds() 
                            # print f

        path = None
        #processing result
        if found:
            path = get_path(final_step) 

        return path
        

# def main(lat1, long1, lat2, long2, start_time):

#     start_node = Node(-1, "start", lat1, long1)
#     goal_node = Node(-2, "goal", lat2, long2)

#     calculator = RouteCalculator(start_node, goal_node, start_time)
#     path = calculator.a_search()

#     print path


#SUFFER NO MORE

# def default(str):
#     return str + ' [Default: %default]'

# def readCommand(argv):
#     from optparse import OptionParser
#     usageStr = """
#     USAGE:      python RouteCalculator.py <options>
#     EXAMPLES:   (1) python RouteCalculator.py -a 5 -b 3 -c 1 -d 2 -s 10
#     """
#     parser = OptionParser(usageStr)
#     parser.add_option('-a', '--lata', dest='lata', type='float',
#         help=default('d'), metavar='LATA', default=0)
#     parser.add_option('-b', '--longa', dest='longa', type='float',
#         help=default('d'), metavar='LONGA', default=0)
#     parser.add_option('-c', '--latb', dest='latb', type='float',
#         help=default('d'), metavar='LATB', default=0)
#     parser.add_option('-d', '--longb', dest='longb', type='float',
#         help=default('d'), metavar='LONGB', default=0)
#     parser.add_option('-s', '--start', dest='start', type='float',
#         help=default('d'), metavar='START', default=0)

#     options, otherjunk = parser.parse_args(argv)
#     if len(otherjunk) != 0:
#         raise Exception('Command line input not understood: ' + str(otherjunk))
#     #parser is incomplete - further enhancement required
#     return options

# if __name__ == '__main__':
#     #args = readCommand(sys.argv[1:])
#     #main(args.lata, args.longa, args.latb, args.longb, args.start)
#     get_results(10, 10, 10, 10, 10)

