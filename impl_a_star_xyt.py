from GLOBALS import *
from impl_g_graph_from_map import build_graph_from_png, build_h_func
from simulator_objects import Agent
from functions import *
from simulator_objects import Node


def update_res_tables(path, res_table, goal_pos_res_table, edge_res_table):
    if path is not None:
        res_table.extend(path)
        goal_pos_res_table.append((path[-1][0], path[-1][1]))
    if len(path) > 2:
        curr_step = path[0]
        for i_step in path[1:]:
            edge_res_table.append((curr_step[0], curr_step[1], i_step[0], i_step[1], i_step[2]))
            curr_step = i_step


def build_the_solution(agent, curr_node):
    if curr_node.ID == agent.goal.ID:
        path = [(curr_node.x, curr_node.y, curr_node.t)]
        while curr_node.parent is not None:
            curr_node = curr_node.parent
            path.append((curr_node.x, curr_node.y, curr_node.t))
        path.reverse()
        return path
    return None


def f_value(e):
    # return e.f() - e.t
    return e.f()


def gen_node(i_node, t):
    new_node = Node(i_node.ID, i_node.x, i_node.y, i_node.neighbours)
    new_node.t = t
    return new_node


def check_conf_and_add(i_node, from_node, t,
                       res_table_vertex, res_table_goal_pos, res_table_edge,
                       node_successors, max_t=1e10):
    res_bool = (i_node.x, i_node.y, t) not in res_table_vertex
    goal_bool = (i_node.x, i_node.y) not in res_table_goal_pos
    edge_bool_backwards = (i_node.x, i_node.y, from_node.x, from_node.y, t) not in res_table_edge
    edge_bool_forward = (from_node.x, from_node.y, i_node.x, i_node.y, t) not in res_table_edge
    t_bool = t < max_t
    if not t_bool:
        print('[CONFLICT]: Time exceeded the allowed margin.')
    if res_bool and goal_bool and edge_bool_forward and edge_bool_backwards and t_bool:
        node_successors.append(gen_node(i_node, t))


def a_star_xyt(agent, nodes, nodes_dict, conf_vertex=None, conf_edge=None, conf_final_pos=None, h_func=None):
    start = time.time()
    res_table_vertex = []  # (x, y, time) - reservation table
    res_table_edge = []  # (x1, y1, x2, y2, time)
    res_table_goal_pos = []  # (x, y)

    if conf_vertex:
        res_table_vertex.extend(conf_vertex)

    if conf_edge:
        res_table_edge.extend(conf_edge)

    if conf_final_pos:
        res_table_goal_pos.extend(conf_final_pos)

    # init
    time_counter = 0
    curr_node = gen_node(agent.start, time_counter)
    curr_node.h = distance_nodes(curr_node, agent.goal, h_func)
    agent.reset()
    agent.open_list.append(curr_node)

    while len(agent.open_list) > 0:
        # print(f'\r{agent.name} open: {len(agent.open_list)}', end='')
        # Take node with the lowest f
        agent.open_list.sort(key=f_value)
        curr_node = agent.open_list.pop(0)

        # check if we found the solution
        if curr_node.name == agent.goal.name:
            curr_node_pos = (curr_node.x, curr_node.y)
            vertex_conf_with_curr_list = [pos[2] for pos in res_table_vertex if (pos[0], pos[1]) == curr_node_pos]
            # if there is a position in the list of vertex conflicts
            if len(vertex_conf_with_curr_list) > 0:
                max_t = max(vertex_conf_with_curr_list)
                # and the time of current pos in greater than one in the table
                if curr_node.t > max_t:
                    break
            # if the position is not in the list of vertex conflicts
            else:
                break

        # generate successors
        time_counter = curr_node.t + 1
        node_successors = []
        # add neighbours
        for nei in curr_node.neighbours:
            check_conf_and_add(nodes_dict[nei], curr_node, time_counter, res_table_vertex, res_table_goal_pos,
                               res_table_edge, node_successors, max_t=len(nodes))
        # add itself
        check_conf_and_add(curr_node, curr_node, time_counter, res_table_vertex, res_table_goal_pos, res_table_edge,
                           node_successors, max_t=len(nodes))

        # loop on successors
        for i_successor in node_successors:
            # check in open list
            if i_successor.name in agent.open_list_names():
                i_successor_in_open = agent.get_from_open_list(i_successor.name)
                if i_successor_in_open.t <= time_counter:
                    continue

            # check in closed list
            # elif i_successor.name in agent.closed_list_names():
            #     i_successor_in_closed = agent.get_from_closed_list(i_successor.name)
            #     g =
            #     if i_successor_in_closed.g <= g:
            #         continue

            i_successor.h = distance_nodes(i_successor, agent.goal, h_func)
            i_successor.g = curr_node.g + 1
            i_successor.parent = curr_node
            agent.open_list.append(i_successor)

        # add current to the closed list
        agent.closed_list.append(curr_node)

        # time constraint
        end = time.time() - start
        if end > 2:
            print(f'\n[CONSTRAINT]: Out of time constraint {end : .2f}.')
            return None

    path = build_the_solution(agent, curr_node)
    # end = time.time() - start
    # if end > 2:
    #     print('more time')
    return path

    # if path is None:
    #     return None
    # update_res_tables(path, res_table_vertex, res_table_goal_pos, res_table_edge)


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    nodes, nodes_dict = build_graph_from_png(image_name)
    h_func = build_h_func(nodes, nodes_dict, image_name)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(n_agents)]
    path = a_star_xyt(agents[0], nodes=nodes, nodes_dict=nodes_dict, h_func=h_func)

    print('There is Solution!😄') if path is not None else print('No Solution ❌')
    print(f'seed: {seed}')
    plot_paths_moving({agents[0].name: path}, nodes, nodes_dict, plot_field=True)


if __name__ == '__main__':
    n_agents = 10
    # with_seed = True
    with_seed = False
    # seed = 6812
    seed = random.randint(0, 10000)
    # image_name = '19_20_warehouse.png'
    image_name = 'den101d.png'
    # image_name = '9_10_no_obstacles.png'
    # image_name = 'lak110d.png'
    # image_name = '2_10_random.png'
    # image_name = '3_10_random.png'
    # image_name = 'den520d.png'
    main()
