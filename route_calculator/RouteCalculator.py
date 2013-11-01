#Anh Nguyen
import util 
import data_structure
import data_manager
import json, sys, random
# import simplejson
from data_manager import *
from data_structure import *

class RouteCalculator:

    def __init__(self, _from, _to, _start_time):
        self.start_node = _from
        self.goal_node = _to
        self.start_time = _start_time

    def a_search(self):
    	found = False
    	resign = False
    	pQueue = PriorityQueue()

    	start_state = State(self.start_node, self.goal_node, self.start_time, self.start_time, None, None)

        # print 'start state'
        # start_state.print_info()

    	pQueue.push(start_state, 0)
    	explored = []
    	final_state = None

    	while not found and not resign:
            if pQueue.isEmpty():
                resign = True
            else:
                current_state = pQueue.pop()
                explored.append(current_state.node.id)

                if current_state.is_goal():
                    found = True
                    final_state = current_state
                    path = get_path(final_state)
                    return path
                else:
                    next_states = get_next_states(current_state)
                    for s in next_states:
                        if (s.node.id not in explored and pQueue.search(s.node) == False):
                            f = (s.arrived_time - start_state.started_time).total_seconds() + s.heuristic() #f = g + h
                            pQueue.push(s, f)

        path = None
        #processing result
        if found:
            path = get_path(final_state)

        return path
        

def main(lat1, long1, lat2, long2, start_time):

    start_node = Node(-1, "start", lat1, long1)
    goal_node = Node(-2, "goal", lat2, long2)

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

