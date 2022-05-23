from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
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
    return e.f()


def gen_node(i_node, t):
    new_node = Node(i_node.ID, i_node.x, i_node.y, i_node.neighbours)
    new_node.t = t
    return new_node


def res_table_check(i_node, from_node, t, res_table, goal_pos_res_table, edge_res_table, node_successors):
    res_bool = (i_node.x, i_node.y, t) not in res_table
    goal_bool = (i_node.x, i_node.y) not in goal_pos_res_table
    edge_bool_backwards = (i_node.x, i_node.y, from_node.x, from_node.y, t) not in edge_res_table
    edge_bool_forward = (from_node.x, from_node.y, i_node.x, i_node.y, t) not in edge_res_table
    t_bool = t < 1e10
    if res_bool and goal_bool and edge_bool_forward and edge_bool_backwards and t_bool:
        node_successors.append(gen_node(i_node, t))


def a_star_xyt(agent, nodes, nodes_dict, vertex_conf=None, edge_conf=None, final_pos_conf=None):
    vertex_res_table = []  # (x, y, time) - reservation table
    edge_res_table = []  # (x, y, x, y, t)
    goal_pos_res_table = []  # (x, y)

    if vertex_conf:
        vertex_res_table.extend(vertex_conf)

    if edge_conf:
        edge_res_table.extend(edge_conf)

    if final_pos_conf:
        goal_pos_res_table.extend(final_pos_conf)

    # init
    time_counter = 0
    curr_node = gen_node(agent.start, time_counter)
    curr_node.h = distance_nodes(curr_node, agent.goal)
    agent.reset()
    agent.open_list.append(curr_node)

    while len(agent.open_list) > 0:
        # print(f'\r{agent.name} open: {len(agent.open_list)}', end='')
        # Take node with the lowest f
        agent.open_list.sort(key=f_value)
        curr_node = agent.open_list.pop(0)

        # check if we found the solution
        if curr_node.ID == agent.goal.ID:
            vertex_table_time_dict = {(pos[0], pos[1]): pos[2] for pos in vertex_res_table}
            curr_node_pos = (curr_node.x, curr_node.y)
            if curr_node_pos in vertex_table_time_dict:
                time_in_table = vertex_table_time_dict[curr_node_pos]
                if curr_node.t > time_in_table:
                    break
            else:
                break

        # generate successors
        time_counter = curr_node.g + 1
        node_successors = []
        for nei in curr_node.neighbours:
            res_table_check(nodes_dict[nei], curr_node, time_counter, vertex_res_table, goal_pos_res_table,
                            edge_res_table, node_successors)
        res_table_check(curr_node, curr_node, time_counter, vertex_res_table, goal_pos_res_table, edge_res_table,
                        node_successors)

        # loop on successors
        for i_successor in node_successors:
            i_successor_curr_cost = curr_node.g + 1
            # check in open list
            if i_successor.ID in agent.open_list_names():
                i_successor_in_open = agent.get_from_open_list(i_successor.ID)
                if i_successor_in_open.g <= i_successor_curr_cost:
                    continue
            # check in closed list
            # elif i_successor.ID in agent.closed_list_names() and ca_star_bool:
            #     i_successor_in_closed = agent.get_from_closed_list(i_successor.ID)
            #     if i_successor_in_closed.g <= i_successor_curr_cost:
            #         continue
            else:
                agent.open_list.append(i_successor)
                i_successor.h = distance_nodes(i_successor, agent.goal)
            i_successor.g = i_successor_curr_cost
            i_successor.parent = curr_node

        # add current to the closed list
        agent.closed_list.append(curr_node)

    path = build_the_solution(agent, curr_node)
    if path is None:
        return None
    update_res_tables(path, vertex_res_table, goal_pos_res_table, edge_res_table)

    return path


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    nodes, nodes_dict = build_graph_from_png(image_name)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(n_agents)]
    path = a_star_xyt(agents[0], nodes=nodes, nodes_dict=nodes_dict)

    print('There is Solution!😄') if path is not None else print('No Solution ❌')
    print(f'seed: {seed}')
    plot_paths_moving({agents[0].name: path}, nodes, nodes_dict, plot_field=True)


if __name__ == '__main__':
    n_agents = 10
    with_seed = True
    # seed = 6812
    seed = random.randint(0, 10000)
    image_name = '19_20_warehouse.png'
    # image_name = '9_10_no_obstacles.png'
    # image_name = 'lak110d.png'
    # image_name = '2_10_random.png'
    # image_name = '3_10_random.png'
    # image_name = 'den520d.png'
    main()
