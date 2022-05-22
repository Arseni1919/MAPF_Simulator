from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from functions import *
from simulator_objects import Agent
from impl_CA_star import ca_star, a_star_xyt


def calc_cbs(num_of_agents, nodes, nodes_dict, start_nodes, goal_nodes):
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(num_of_agents)]
    paths = run_cbs(agents, nodes=nodes, nodes_dict=nodes_dict)
    paths, solution_bool = check_validity(paths)
    return paths, solution_bool


class CTNode:
    def __init__(self, agents, nodes, nodes_dict, vertex_conf=None, edge_conf=None):
        self.agents = agents
        self.nodes = nodes
        self.nodes_dict = nodes_dict

        if vertex_conf:
            self.vertex_conf = copy.deepcopy(vertex_conf)
        else:
            self.vertex_conf = {agent.name: [] for agent in agents}

        if edge_conf:
            self.edge_conf = copy.deepcopy(edge_conf)
        else:
            self.edge_conf = {agent.name: [] for agent in agents}

        self.solution = {}
        self.cost = 1e10
        self.infinity = 1e10
        self.parent = None
        self.children = None

    def insert_vertex_conf(self, vertex_dict):
        for name, conf in vertex_dict.items():
            if conf not in self.vertex_conf[name]:
                self.vertex_conf[name].append(conf)
            # else:
            #     print('fuck')

    def insert_edge_conf(self, edge_dict):
        for name, conf in edge_dict.items():
            if conf not in self.edge_conf[name]:
                self.edge_conf[name].append(conf)
            # else:
            #     print('fuck')

    def create_solution(self):
        for agent in self.agents:
            # if agent.name == 'agent_8' and (12, 10, 6) in self.vertex_conf['agent_8']:
            #     print('here')
            path = a_star_xyt(agent, self.nodes, self.nodes_dict,
                              self.vertex_conf[agent.name], self.edge_conf[agent.name])
            if path is not None:
                self.solution[agent.name] = path
                self.cost = get_cost(self.solution)


def get_edge_list(path):
    edges_list = []
    curr_pos = path[0]
    for next_pos in path[1:]:
        edges_list.append((curr_pos[0], curr_pos[1], next_pos[0], next_pos[1], next_pos[2]))
        curr_pos = next_pos
    return edges_list


def validate_paths_until_first_conflict(node):
    # print('start validating...')
    agents_names = list(node.solution.keys())
    long_paths = lengthen_paths(node.solution)
    for agent_name_1, agent_name_2 in combinations(agents_names, 2):
        # if agent_name_1 == 'agent_8':
        #     print(agent_name_1)
        # print(agent_name_1, agent_name_2)
        # vertex
        path_1 = long_paths[agent_name_1]
        path_2 = long_paths[agent_name_2]
        for pos in path_1:
            if pos in path_2:
                vertex_conf = (agent_name_1, agent_name_2), pos
                edge_conf = None
                return vertex_conf, edge_conf

        # edges
        path_1 = node.solution[agent_name_1]
        path_2 = node.solution[agent_name_2]
        if len(path_1) > 1 and len(path_2) > 1:
            edges_list_1 = get_edge_list(path_1)
            edges_list_2 = get_edge_list(path_2)
            for edge in edges_list_1:
                # 0 - x, 1 - y, 2 - x, 3 - y, 4 - t
                reversed_edge = (edge[2], edge[3], edge[0], edge[1], edge[4])
                if reversed_edge in edges_list_2:
                    vertex_conf = None
                    edge_conf = (agent_name_1, agent_name_2), {agent_name_1: edge, agent_name_2: reversed_edge}
                    # edge_conf = (agent_name_1, agent_name_2), {agent_name_1: reversed_edge, agent_name_2: edge}
                    return vertex_conf, edge_conf
    return None, None


def run_cbs(agents, nodes, nodes_dict):
    infinity = 1e10
    root_node = CTNode(agents, nodes, nodes_dict)
    root_node.create_solution()
    open_list = [root_node]
    while len(open_list) > 0:
        # print(f'\ropen list: {len(open_list)}', end='')
        # best node
        open_list.sort(key=lambda x: x.cost)
        curr_node = open_list.pop(0)
        # if len(open_list) > 72:
            # print('here 1')
        # if (12, 10, 6) in curr_node.vertex_conf['agent_8']:
            # print('here 2')

        # validate
        vertex_conf, edge_conf = validate_paths_until_first_conflict(curr_node)
        # print(f'\n---\nvertex: {vertex_conf}, \nedge: {edge_conf} \n ---')
        if vertex_conf is None and edge_conf is None:
            # return solution
            return curr_node.solution

        # VERTEX CONFLICT
        if vertex_conf is not None:
            # first conflict
            agents_names_in_conflict, pos = vertex_conf

            # for each agent in conflict
            for agent_name in agents_names_in_conflict:
                new_node = CTNode(agents, nodes, nodes_dict, curr_node.vertex_conf, curr_node.edge_conf)
                vertex_dict = {agent_name: pos}
                new_node.insert_vertex_conf(vertex_dict)
                new_node.create_solution()

                # insert to open list
                if new_node.cost < infinity:
                    # print(f'node cost: {new_node.cost}')
                    open_list.append(new_node)
                    # if len(open_list) > 73:
                    #     print('###########')
                    #     print(f'\n--- Curr node:\nvertex: {curr_node.vertex_conf}, \nedge: {curr_node.edge_conf} \n ---')
                    #     print(f'\n--- New node:\nvertex: {new_node.vertex_conf}, \nedge: {new_node.edge_conf} \n ---')

        # EDGE CONFLICT
        if edge_conf is not None:
            # first conflict
            agents_names_in_conflict, edge_conf_dict = edge_conf

            # for each agent in conflict
            for agent_name in agents_names_in_conflict:
                new_node = CTNode(agents, nodes, nodes_dict, curr_node.vertex_conf, curr_node.edge_conf)
                edge_dict = {agent_name: edge_conf_dict[agent_name]}
                # print(edge_conf_dict[agent_name])
                new_node.insert_edge_conf(edge_dict)
                new_node.create_solution()

                # insert to open list
                if new_node.cost < infinity:
                    open_list.append(new_node)

    return None


def main():
    if with_seed:
        np.random.seed(seed)
        random.seed(seed)
        print(f'seed: {seed}')

    nodes, nodes_dict = build_graph_from_png(image_name)
    start_nodes, goal_nodes = get_random_start_and_goal_positions(nodes, n_agents)
    agents = [Agent(i, start=start_nodes[i], goal=goal_nodes[i]) for i in range(n_agents)]
    paths = run_cbs(agents, nodes=nodes, nodes_dict=nodes_dict)

    paths, solution_bool = check_validity(paths)
    print('There is Solution!😄') if solution_bool else print('No Solution ❌')
    print(f'seed: {seed}')
    plot_paths_moving(paths, nodes, nodes_dict, plot_field=True)


if __name__ == '__main__':
    n_agents = 13
    with_seed = True
    seed = 211
    # seed = random.randint(0, 10000)
    image_name = '19_20_warehouse.png'
    # image_name = '9_10_no_obstacles.png'
    # image_name = 'lak110d.png'
    # image_name = '2_10_random.png'
    # image_name = '3_10_random.png'
    # image_name = 'den520d.png'
    main()
