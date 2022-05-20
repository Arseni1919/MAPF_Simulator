from GLOBALS import *
from impl_graph_from_map import build_graph_from_png
from functions import *
from simulator_objects import Agent
from impl_CA_star import ca_star


class CTNode:
    def __init__(self, agents, nodes, nodes_dict, vertex_conf=None, edge_conf=None):
        self.agents = agents
        self.nodes = nodes
        self.nodes_dict = nodes_dict

        if vertex_conf:
            self.vertex_conf = vertex_conf
        else:
            self.vertex_conf = {agent.name: [] for agent in agents}

        if edge_conf:
            self.edge_conf = edge_conf
        else:
            self.edge_conf = {agent.name: [] for agent in agents}

        self.solution = {}
        self.cost = 1e10
        self.infinity = 1e10
        self.parent = None
        self.children = None

    def create_solution(self):
        for agent in self.agents:
            path = ca_star([agent], self.nodes, self.nodes_dict,
                           self.vertex_conf[agent.name], self.edge_conf[agent.name])[agent.name]
            if path is not None:
                self.solution[agent.name] = path
                self.cost = get_cost(self.solution)

    def insert_vertex_conf(self, vertex_dict):
        for name, conf in vertex_dict.items():
            self.vertex_conf[name].append(conf)


def validate_paths_until_first_conflict(node):
    agents_names = list(node.solution.keys())
    for agent_name_1, agent_name_2 in combinations(agents_names, 2):
        path_1 = node.solution[agent_name_1]
        path_2 = node.solution[agent_name_2]
        for pos in path_1:
            if pos in path_2:
                return (agent_name_1, agent_name_2), pos
    return None


def run_cbs(agents, nodes, nodes_dict):
    infinity = 1e10
    root_node = CTNode(agents, nodes, nodes_dict)
    root_node.create_solution()
    open_list = [root_node]
    while len(open_list) > 0:
        # best node
        open_list.sort(key=lambda x: x.cost)
        curr_node = open_list.pop(0)

        # validate
        conflict = validate_paths_until_first_conflict(curr_node)
        if conflict is None:
            # return solution
            return curr_node.solution

        # first conflict
        agents_names_in_conflict, pos = conflict

        # for each agent in conflict
        for agent_name in agents_names_in_conflict:
            vertex_dict = {agent_name: pos}
            new_node = CTNode(agents, nodes, nodes_dict, curr_node.vertex_conf, curr_node.edge_conf)
            new_node.insert_vertex_conf(vertex_dict)
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
    n_agents = 10
    with_seed = True
    seed = 6812
    # seed = random.randint(0, 10000)
    image_name = '19_20_warehouse.png'
    # image_name = '9_10_no_obstacles.png'
    # image_name = 'lak110d.png'
    # image_name = '2_10_random.png'
    # image_name = '3_10_random.png'
    # image_name = 'den520d.png'
    main()
