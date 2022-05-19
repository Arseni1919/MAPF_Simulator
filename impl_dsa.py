from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from functions import *
from simulator_objects import LSNode
from impl_CA_star import ca_star


def create_local_search_nodes(n_vars, start_nodes, goal_nodes, nodes, nodes_dict):
    agents_nodes = []
    graph = {}

    # create agents
    for i in range(n_vars):
        var_node = LSNode(i, start=start_nodes[i], goal=goal_nodes[i], nodes=nodes, nodes_dict=nodes_dict, a_star_func=ca_star)
        agents_nodes.append(var_node)
        graph[var_node.name] = var_node

    # set neighbours
    comb_list = list(combinations(agents_nodes, 2))
    for var1, var2 in comb_list:
        var1.nei_nodes.append(var2)
        var2.nei_nodes.append(var1)

    return agents_nodes


def run_dsa(agents_nodes):
    for agent in agents_nodes:
        agent.init()
    for iteration in range(n_iterations):
        for agent in agents_nodes:
            agent.send_messages(iteration)
        for agent in agents_nodes:
            agent.dsa_update_path(iteration)

    # paths: {'agent name': [(x, y, t), ...], ...}
    paths = {agent.name: agent.path for agent in agents_nodes}
    paths, solution_bool = check_validity(paths)
    return paths, solution_bool


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)

    nodes, nodes_dict = build_graph_from_png(IMAGE_NAME)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    # var_nodes, func_nodes, graph = create_factor_graph(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)
    agents_nodes = create_local_search_nodes(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)
    paths, solution_bool = run_dsa(agents_nodes)  # paths: {'agent name': [(x, y, t), ...], ...}

    print('There is Solution!😄') if solution_bool else print('No Solution ❌')
    print(f'seed: {seed}')
    # plot_paths(paths, nodes, nodes_dict, plot_field=False)
    plot_paths_moving(paths, nodes, nodes_dict, plot_field=True)


if __name__ == '__main__':
    n_agents = 10
    n_iterations = 50
    # with_seed = False
    with_seed = True
    # seed = 11
    seed = random.randint(0, 1000)
    IMAGE_NAME = '9_10_no_obstacles.png'
    main()