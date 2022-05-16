from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from impl_CA_star import ca_star
from simulator_objects import FGVarNode, FGFuncNode
from functions import *


def create_factor_graph(n_vars, start_nodes, goal_nodes, nodes, nodes_dict):
    graph = {}
    var_nodes = []
    func_nodes = []

    # create var nodes
    for i in range(n_vars):
        var_node = FGVarNode(i, start=start_nodes[i], goal=goal_nodes[i])
        var_nodes.append(var_node)
        graph[var_node.name] = var_node

    # create func nodes and add them to var nodes
    comb_list = list(combinations(var_nodes, 2))
    for var1, var2 in comb_list:
        # print(f'{var1.name} - {var2.name}')
        func_node = FGFuncNode((var1, var2))
        var1.nei_fg_func_nodes.append(func_node)
        var2.nei_fg_func_nodes.append(func_node)
        func_nodes.append(func_node)
        graph[func_node.name] = func_node

    # create domains
    for var_node in var_nodes:
        first_path = ca_star([var_node], nodes, nodes_dict)[var_node.name]
        opt_counter = 1
        var_node.domain[f'opt_{opt_counter}'] = first_path
        for pos in first_path[1:]:
            possible_paths = ca_star([var_node], nodes, nodes_dict, res_table_adding=[pos])
            if possible_paths:
                opt_counter += 1
                another_path = possible_paths[var_node.name]
                var_node.domain[f'opt_{opt_counter}'] = another_path
        print(var_node.domain)

    return var_nodes, func_nodes, graph


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)

    nodes, nodes_dict = build_graph_from_png(IMAGE_NAME)
    start_nodes = np.random.choice(nodes, size=n_agents)
    goal_nodes = np.random.choice(nodes, size=n_agents)

    var_nodes, func_nodes, graph = create_factor_graph(n_agents, start_nodes, goal_nodes, nodes, nodes_dict)

    print(graph)


if __name__ == '__main__':
    n_agents = 2
    # with_seed = False
    with_seed = True
    seed = 11
    IMAGE_NAME = '9_10_no_obstacles.png'
    main()
