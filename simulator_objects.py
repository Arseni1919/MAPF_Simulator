from GLOBALS import *


class Node:
    def __init__(self, ID, x, y, neighbours):
        self.ID = ID
        self.x = x
        self.y = y
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
        return [node.ID for node in self.open_list]

    def closed_list_names(self):
        return [node.ID for node in self.closed_list]

    def get_from_open_list(self, name):
        for node in self.open_list:
            if node.ID == name:
                return node
        raise ValueError('no such ID - open list')

    def get_from_closed_list(self, name):
        for node in self.closed_list:
            if node.ID == name:
                return node
        raise ValueError('no such ID - closed list')


class FGVarNode(Agent):
    def __init__(self, agent_id, x=-1, y=-1, start=None, goal=None):
        super(FGVarNode, self).__init__(agent_id, x, y, start, goal)
        self.nei_fg_func_nodes = []
        self.domain = {}
        self.messages = {}

    def send_messages(self, iteration):
        iter_name = f'iter_{iteration}'
        message = {opt_name: 0 for opt_name, path in self.domain.items()}
        if iteration == 0:
            for to_func_node in self.nei_fg_func_nodes:
                if iter_name not in to_func_node.messages:
                    to_func_node.messages[iter_name] = {}
                to_func_node.messages[iter_name][self.name] = message
        else:
            prev_messages = self.messages[f'iter_{iteration - 1}']
            for to_func_node in self.nei_fg_func_nodes:

                # aggregate
                for from_func_name, prev_message in prev_messages.items():
                    if from_func_name != to_func_node.name:
                        for opt_name, _ in message.items():
                            message[opt_name] += prev_message[opt_name]

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
            if step in path_2:
                return self.infinity
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
                    row_values.append(cell_value + message_value)
                message[opt_name_1] = min(row_values)

            min_value = min(list(message.values()))
            message = {opt_name: value - min_value for opt_name, value in message.items()}
            # insert
            if iter_name not in var_1.messages:
                var_1.messages[iter_name] = {}
            var_1.messages[iter_name][self.name] = message



