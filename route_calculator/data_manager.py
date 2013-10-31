import data_structure

def get_next_steps(current_state):
    sql_helper = SqlHelper(HOST, DBNAME, USERNAME, PASSWORD)
    #2 steps:
    #step 1: query mysql, table "schedule" for node.nodeID
    #mysql return all fixed "bus-step" that can be processed.
    bus_steps = sql_helper.get_next_bus_steps(current_state)

    #step2: also query google map for walking-step
    walking_steps = sql_helper.get_next_walking_steps(current_state)

    return (bus_steps + walking_steps)

#Generate possible states by consider possible ways to get from 1 States to available nodes around
def get_next_states(current_state):
    # next_nodes = util.get_avai_nodes()
    # dist_list = dict()
    # for n in next_nodes:
    #   d = util.distance(n, self.node)
    #   dist_list[str(d)] = n

    # #[(distance, node), ...]
    # sorted_dist = sorted(dist_list.items(), key=lambda t: t[0])

    # #get the nearest state in term of time cost
    next_steps = get_next_steps(current_state)
    next_states = [] #util.PriorityQueue()

    for step in next_steps:
        new_started_time = step.start_time
        new_arrived_time = new_started_time + (step.end_time - step.start_time)
        new_node = step.end_node
        new_state = State(new_node, current_state.goal_node, new_started_time, new_arrived_time, step, current_state)
        next_states.append(new_state) #push(new_state, (new_arrived_time - new_started_time)) #push to priority queue

    return next_states

#get path from start to goal
def get_path(final_state):
    prv = final_state
    path = []
    while prv.previous_state != None:
        path.append(prv.previous_step)
        prv = prv.previous_state

    path.reverse()

    string = ""
    for i, p in enumerate(path):
        

        f = p.start_node.name
        t = p.end_node.name
        time1 = p.start_time
        ty = p.type
        
        string += f + ','+t+','+str(time1)+','+ty+"\n"

    return string