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
