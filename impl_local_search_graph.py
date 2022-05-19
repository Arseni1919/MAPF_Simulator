from GLOBALS import *
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
