from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from impl_factor_graph import create_factor_graph
from functions import *


def check_validity(paths):
    return None


def run_max_sum(var_nodes, func_nodes, graph):
    paths = {}
    num_of_iterations = 20
    for iteration in range(num_of_iterations):
        for var_node in var_nodes:
            var_node.send_messages(iteration)
        for func_node in func_nodes:
            func_node.send_messages(iteration)
    for var_node in var_nodes:
        paths[var_node.name] = var_node.get_path(num_of_iterations)
    # paths = check_validity(paths)
    return paths


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)

    nodes, nodes_dict = build_graph_from_png(IMAGE_NAME)
    start_nodes = np.random.choice(nodes, size=n_agents)
    goal_nodes = np.random.choice(nodes, size=n_agents)

    var_nodes, func_nodes, graph = create_factor_graph(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)

    paths = run_max_sum(var_nodes, func_nodes, graph)  # paths: {'agent name': [(x, y, t), ...], ...}

    if paths is None:
        print('No Solution')
    else:
        print(paths)
        plot_paths(paths, nodes, nodes_dict)
        # plot_paths_plotly(paths, nodes, nodes_dict)


if __name__ == '__main__':
    n_agents = 7
    with_seed = False
    # with_seed = True
    seed = 11
    IMAGE_NAME = '9_10_no_obstacles.png'
    main()
