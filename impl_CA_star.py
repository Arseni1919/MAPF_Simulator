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
        while curr_node.ID != agent.start.ID:
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
    # if i_node.x == 3 and i_node.y == 5:
    #     print('stop')
    return new_node


def res_table_check(i_node, from_node, t, res_table, goal_pos_res_table, edge_res_table, node_successors):
    res_bool = (i_node.x, i_node.y, t) not in res_table
    goal_bool = (i_node.x, i_node.y) not in goal_pos_res_table
    edge_bool = (i_node.x, i_node.y, from_node.x, from_node.y, t) not in edge_res_table
    t_bool = t < 1e10
    if res_bool and goal_bool and edge_bool and t_bool:
        node_successors.append(gen_node(i_node, t))


def ca_star(agents, nodes, nodes_dict, res_table_adding=None):

    res_table = []  # (x, y, time) - reservation table
    goal_pos_res_table = []
    edge_res_table = []
    paths = {}

    if res_table_adding:
        res_table.extend(res_table_adding)

    for agent in agents:

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
                break

            # generate successors
            time_counter = curr_node.g + 1
            node_successors = []
            for nei in curr_node.neighbours:
                res_table_check(nodes_dict[nei], curr_node, time_counter, res_table, goal_pos_res_table, edge_res_table, node_successors)
            res_table_check(curr_node, curr_node, time_counter, res_table, goal_pos_res_table, edge_res_table, node_successors)

            # loop on successors
            for i_successor in node_successors:
                i_successor_curr_cost = curr_node.g + 1
                if i_successor.ID in agent.open_list_names():
                    i_successor_in_open = agent.get_from_open_list(i_successor.ID)
                    if i_successor_in_open.g <= i_successor_curr_cost:
                        continue
                elif i_successor.ID in agent.closed_list_names():
                    i_successor_in_closed = agent.get_from_closed_list(i_successor.ID)
                    if i_successor_in_closed.g <= i_successor_curr_cost:
                        continue
                else:
                    agent.open_list.append(i_successor)
                    i_successor.h = distance_nodes(i_successor, agent.goal)
                i_successor.g = i_successor_curr_cost
                i_successor.parent = curr_node

            # add current to the closed list
            agent.closed_list.append(curr_node)

        paths[agent.name] = build_the_solution(agent, curr_node)
        if paths[agent.name] is None:
            return None
        update_res_tables(paths[agent.name], res_table, goal_pos_res_table, edge_res_table)

    return paths


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)

    nodes, nodes_dict = build_graph_from_png(image_name)
    start_nodes = np.random.choice(nodes, size=n_agents)
    goal_nodes = np.random.choice(nodes, size=n_agents)
    agents = []
    for i in range(n_agents):
        agents.append(Agent(i, start=start_nodes[i], goal=goal_nodes[i]))
    paths = ca_star(agents, nodes=nodes, nodes_dict=nodes_dict)

    if paths is None:
        print('No Solution')
    else:
        print(paths)
        # plot_paths_moving(paths, nodes, nodes_dict)
        plot_paths_static(paths, nodes, nodes_dict)
        # plot_paths_plotly(paths, nodes, nodes_dict)


if __name__ == '__main__':
    n_agents = 1
    with_seed = False
    # with_seed = True
    seed = 11
    # image_name = '10_10_random.png'
    # image_name = '9_10_no_obstacles.png'
    image_name = 'lak110d.png'
    # image_name = '2_10_random.png'
    # image_name = '3_10_random.png'
    # image_name = 'den520d.png'
    main()


# plt.scatter(x_items, y_items, marker='s', color='gray', s=100.0)
# # plot paths
# for agent_name, path in paths.items():
#     x_items = [i[0] for i in path]
#     y_items = [i[1] for i in path]
#     plt.plot(x_items, y_items, linestyle='-', marker='p', markersize=20.0, alpha=0.5)
#     plt.text(path[0][0], path[0][1], f'{agent_name}\nstart', dict(size=5), bbox={'facecolor': 'yellow', 'alpha': 1, 'pad': 2})
#     plt.text(path[-1][0], path[-1][1], f'{agent_name}\ngoal', dict(size=5), bbox={'facecolor': 'yellow', 'alpha': 1, 'pad': 2})
#
# plt.show()
