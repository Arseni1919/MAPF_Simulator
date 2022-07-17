from GLOBALS import *
from impl_g_graph_from_map import build_graph_from_png
from simulator_objects import Agent
from functions import *
from simulator_objects import Node
from impl_a_star_xyt import update_res_tables, build_the_solution, f_value, gen_node, check_conf_and_add


def calc_ca_star(num_of_agents, nodes, nodes_dict, start_nodes, goal_nodes, h_func=None):
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(num_of_agents)]
    paths = ca_star(agents, nodes=nodes, nodes_dict=nodes_dict, h_func=h_func)
    if paths is not None:
        paths, solution_bool = check_validity(paths)
        return paths, solution_bool
    return paths, False


def ca_star(agents, nodes, nodes_dict,
            res_table_adding=None, edge_res_table_adding=None, goal_pos_adding=None, h_func=None):

    vertex_res_table = []  # (x, y, time) - reservation table
    edge_res_table = []  # (x, y, x, y, t)
    goal_pos_res_table = []  # (x, y)
    paths = {}

    if res_table_adding:
        vertex_res_table.extend(res_table_adding)

    if edge_res_table_adding:
        edge_res_table.extend(edge_res_table_adding)

    if goal_pos_adding:
        goal_pos_res_table.extend(goal_pos_adding)

    for agent in agents:

        # init
        time_counter = 0
        curr_node = gen_node(agent.start, time_counter)
        curr_node.h = distance_nodes(curr_node, agent.goal, h_func=h_func)
        agent.reset()
        agent.open_list.append(curr_node)

        while len(agent.open_list) > 0:
            # print(f'\r{agent.name} open: {len(agent.open_list)}', end='')
            # Take node with the lowest f
            agent.open_list.sort(key=f_value)
            curr_node = agent.open_list.pop(0)

            # check if we found the solution
            if curr_node.ID == agent.goal.ID:
                break

            # generate successors
            time_counter = curr_node.g + 1
            node_successors = []
            for nei in curr_node.neighbours:
                check_conf_and_add(nodes_dict[nei], curr_node, time_counter, vertex_res_table, goal_pos_res_table, edge_res_table, node_successors)
            check_conf_and_add(curr_node, curr_node, time_counter, vertex_res_table, goal_pos_res_table, edge_res_table, node_successors)

            # loop on successors
            for i_successor in node_successors:
                i_successor_curr_cost = curr_node.g + 1
                # check in open list
                if i_successor.name in agent.open_list_names():
                    i_successor_in_open = agent.get_from_open_list(i_successor.name)
                    if i_successor_in_open.g <= i_successor_curr_cost:
                        continue
                # check in closed list
                elif i_successor.name in agent.closed_list_names():
                    i_successor_in_closed = agent.get_from_closed_list(i_successor.name)
                    if i_successor_in_closed.g <= i_successor_curr_cost:
                        continue
                else:
                    agent.open_list.append(i_successor)
                    i_successor.h = distance_nodes(i_successor, agent.goal, h_func)
                i_successor.g = i_successor_curr_cost
                i_successor.parent = curr_node

            # add current to the closed list
            agent.closed_list.append(curr_node)

        paths[agent.name] = build_the_solution(agent, curr_node)
        if paths[agent.name] is None:
            return None
        update_res_tables(paths[agent.name], vertex_res_table, goal_pos_res_table, edge_res_table)

    return paths


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    nodes, nodes_dict = build_graph_from_png(image_name)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(n_agents)]
    paths = ca_star(agents, nodes=nodes, nodes_dict=nodes_dict)

    paths, solution_bool = check_validity(paths)
    print('There is Solution!😄') if solution_bool else print('No Solution ❌')
    print(f'seed: {seed}')
    plot_paths_moving(paths, nodes, nodes_dict, plot_field=True)


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

