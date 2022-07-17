import copy

from GLOBALS import *
from functions import get_collisions, lengthen_paths


class Node:
    def __init__(self, ID, x, y, neighbours):
        self.ID = ID
        self.x = x
        self.y = y
        self.name = f'{self.x}_{self.y}'
        self.neighbours = neighbours
        self.parent = None
        self.g = 0
        self.h = 0
        self.t = 0

    def f(self):
        return self.g + self.h


class Agent:
    def __init__(self, agent_id, x=-1, y=-1, start=None, goal=None):
        self.id = agent_id
        self.x, self.y = x, y
        self.start = start
        self.goal = goal
        self.open_list = []
        self.closed_list = []
        self.name = f'agent_{agent_id}'

    def reset(self):
        self.open_list = []
        self.closed_list = []

    def open_list_names(self):
        return [node.name for node in self.open_list]

    def closed_list_names(self):
        return [node.name for node in self.closed_list]

    def get_from_open_list(self, name):
        for node in self.open_list:
            if node.name == name:
                return node
        raise ValueError('no such ID - open list')

    def get_from_closed_list(self, name):
        for node in self.closed_list:
            if node.name == name:
                return node
        raise ValueError('no such ID - closed list')


# Local Search Node
class LSNode(Agent):
    def __init__(self, agent_id, x=-1, y=-1, start=None, goal=None, nodes=None, nodes_dict=None, a_star_func=None):
        super(LSNode, self).__init__(agent_id, x, y, start, goal)
        self.nei_nodes = []
        self.nodes = nodes
        self.nodes_dict = nodes_dict
        self.a_star_func = a_star_func
        self.path = []
        self.lr_path = []
        self.messages = {}
        self.lr_messages = {}
        self.infinity = 1e10
        self.lr = self.infinity

    def init(self, h_func):
        self.path = self.a_star_func(self, self.nodes, self.nodes_dict, h_func=h_func)

    def send_messages(self, iteration):
        iter_name = f'iter_{iteration}'
        for nei in self.nei_nodes:
            if iter_name not in nei.messages:
                nei.messages[iter_name] = {}
            nei.messages[iter_name][self.name] = self.path

    def count_vertex_conflicts(self, paths):
        conf_list = []
        for agent_name, path in paths.items():
            for pos in self.path:
                if pos in path:
                    conf_list.append(pos)
        return conf_list

    def count_edge_conflicts(self, paths):
        # build big list
        edge_big_list = []
        for agent_name, path in paths.items():
            if len(path) > 1:
                curr_pos = path[0]
                for next_pos in path[1:]:
                    edge_big_list.append((curr_pos[0], curr_pos[1], next_pos[0], next_pos[1], next_pos[2]))
                    curr_pos = next_pos
        # count conflicts
        conf_list = []
        if len(self.path) > 1:
            curr_pos = self.path[0]
            for next_pos in self.path[1:]:
                edge = (next_pos[0], next_pos[1], curr_pos[0], curr_pos[1], next_pos[2])
                if edge in edge_big_list:
                    conf_list.append(edge)
                curr_pos = next_pos

        return conf_list

    def my_confs_with_others(self, paths):
        l_paths = lengthen_paths(paths)
        vertex_conf_list = self.count_vertex_conflicts(l_paths)
        edge_conf_list = self.count_edge_conflicts(paths)
        if len(edge_conf_list) > 0:
            pass
        return vertex_conf_list, edge_conf_list

    @staticmethod
    def all_paths_to_confs(paths):
        l_paths = lengthen_paths(paths)
        # vertexes
        vertex_conf_list, edge_conf_list = [], []
        # VERTEX CONF
        for agent_name, path in l_paths.items():
            vertex_conf_list.extend(path)
        # EDGE CONF
        for agent_name, path in paths.items():
            if len(path) > 1:
                curr_pos = path[0]
                for next_pos in path[1:]:
                    edge_conf_list.append((next_pos[0], next_pos[1], curr_pos[0], curr_pos[1], next_pos[2]))
                    curr_pos = next_pos
        return vertex_conf_list, edge_conf_list

    def dsa_update_path(self, iteration, h_func=None):
        iter_name = f'iter_{iteration}'
        last_messages = self.messages[iter_name]
        vertex_conf_list, edge_conf_list = self.my_confs_with_others(last_messages)
        other_vertexes, other_edges = self.all_paths_to_confs(last_messages)
        vertex_conf_list.extend(other_vertexes)
        edge_conf_list.extend(other_edges)
        # if self.id == 7:
        #     print('stop')
        if len(vertex_conf_list) + len(edge_conf_list) > 0:
            # dsa condition
            if random.random() < 0.8:
                a_star_path = self.a_star_func(self, self.nodes, self.nodes_dict,
                                               vertex_conf_list, edge_conf_list, h_func=h_func)
                if a_star_path is not None:
                    self.path = a_star_path
                else:
                    print(f'!!! No path was found for {self.name} in iteration {iteration}.')
                # vertex_conf_list, edge_conf_list = self.my_confs_with_others(self.messages[iter_name])
                # print('', end='')

    def mgm_send_lr_messages(self, iteration, h_func=None):
        iter_name = f'iter_{iteration}'
        last_messages = self.messages[iter_name]

        # calculate LR
        self.lr = self.infinity
        self.lr_path = self.path
        vertex_conf_list, edge_conf_list = self.my_confs_with_others(last_messages)
        other_vertexes, other_edges = self.all_paths_to_confs(last_messages)
        vertex_conf_list.extend(other_vertexes)
        edge_conf_list.extend(other_edges)
        if len(vertex_conf_list) + len(edge_conf_list) > 0:
            # if self.id == 7:
            #     print('stop')
            new_path = self.a_star_func(self, self.nodes, self.nodes_dict,
                                        vertex_conf_list, edge_conf_list, h_func=h_func)
            if new_path is not None:
                self.lr_path = new_path
                self.lr = len(self.lr_path) - len(self.path)
            else:
                print(f'!!! No path was found for {self.name} in iteration {iteration}.')

        # send LR messages
        for nei in self.nei_nodes:
            if iter_name not in nei.lr_messages:
                nei.lr_messages[iter_name] = {}
            nei.lr_messages[iter_name][self.name] = self.lr

    def mgm_update_path(self, iteration):
        iter_name = f'iter_{iteration}'
        last_lr_messages = self.lr_messages[iter_name]
        min_lr = min(list(last_lr_messages.values()))
        min_lr_agents = [agent for agent in self.nei_nodes if last_lr_messages[agent.name] == min_lr]
        min_lr_agents_index = min([agent.id for agent in min_lr_agents])
        if self.lr < self.infinity:
            if self.lr < min_lr or self.lr == min_lr and self.id < min_lr_agents_index:
                self.path = self.lr_path
                # vertex_conf_list, edge_conf_list = self.get_conf_lists(self.messages[iter_name])
                # print(f' mgm change - {self.name}')


# Factor Graph Nodes
class FGVarNode(Agent):
    def __init__(self, agent_id, x=-1, y=-1, start=None, goal=None):
        super(FGVarNode, self).__init__(agent_id, x, y, start, goal)
        self.nei_fg_func_nodes = []
        self.domain = {}
        self.r_values = {}
        self.messages = {}

    def add_to_domain(self, opt_name, path):
        self.domain[opt_name] = path
        self.r_values[opt_name] = random.random() / 1000

    def send_messages(self, iteration):
        iter_name = f'iter_{iteration}'
        message = {opt_name: 0 for opt_name, path in self.domain.items()}
        for to_func_node in self.nei_fg_func_nodes:
            if iteration != 0:
                prev_messages = self.messages[f'iter_{iteration - 1}']

                # aggregate
                for from_func_name, prev_message in prev_messages.items():
                    if from_func_name != to_func_node.name:
                        for opt_name, _ in message.items():
                            message[opt_name] += prev_message[opt_name]

                # alpha correction
                min_value = min(list(message.values()))
                message = {opt_name: value - min_value for opt_name, value in message.items()}

            # insert
            if iter_name not in to_func_node.messages:
                to_func_node.messages[iter_name] = {}
            to_func_node.messages[iter_name][self.name] = message

    def get_path(self, iteration):
        total_values = {opt_name: 0 for opt_name, path in self.domain.items()}
        for func_name, opt_dict in self.messages[f'iter_{iteration - 1}'].items():
            for opt_name, value in opt_dict.items():
                total_values[opt_name] += value
        min_opt_name = min(total_values, key=total_values.get)
        return self.domain[min_opt_name]


# Factor Graph Nodes
class FGFuncNode:
    def __init__(self, nei_fg_var_nodes):
        self.nei_fg_var_nodes = nei_fg_var_nodes
        name = 'func'
        for var in self.nei_fg_var_nodes:
            name = f'{name}-{var.name}'
        self.name = name
        self.messages = {}
        self.infinity = 1e10

    def combine(self, path_1, path_2):
        cell_value = len(path_1) + len(path_2)
        for step in path_1:

            # vertex conflict
            if step in path_2:
                return self.infinity

            # final location conflict
            # if (step[0], step[1]) == (path_2[-1][0], path_2[-1][1]):
            #     return self.infinity

            # edge conflict

        return cell_value

    def send_messages(self, iteration):
        iter_name = f'iter_{iteration}'
        for var_1, var_2 in permutations(self.nei_fg_var_nodes, 2):
            message = {opt_name: 0 for opt_name, path in var_1.domain.items()}
            for opt_name_1, path_1 in var_1.domain.items():
                row_values = []
                for opt_name_2, path_2 in var_2.domain.items():
                    cell_value = self.combine(path_1, path_2)
                    message_value = self.messages[iter_name][var_2.name][opt_name_2]
                    r_val_1 = var_1.r_values[opt_name_1]
                    r_val_2 = var_2.r_values[opt_name_2]
                    row_values.append(cell_value + message_value + r_val_1 + r_val_2)
                message[opt_name_1] = min(row_values)

            # # alpha correction
            # min_value = min(list(message.values()))
            # message = {opt_name: value - min_value for opt_name, value in message.items()}

            # insert
            if iter_name not in var_1.messages:
                var_1.messages[iter_name] = {}
            var_1.messages[iter_name][self.name] = message



