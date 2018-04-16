from enum import Enum
from collections import deque

class SubstructNodeType(Enum):
    ACCESS = 1
    DEREF = 2
    NAME = 3
    INDEX = 4
    ADDRESS = 5

class SubstructNode:
    def __init__(self, node_type, data=None):
        self.node_type = node_type
        self.data = data

class SubstrctBuilder:
    def __init__(self):
        self.nodes = []

    def add_name(self, name):
        self.nodes.append(SubstructNode(SubstructNodeType.NAME, name))

    def add_arrow(self):
        self.nodes.append(SubstructNode(SubstructNodeType.DEREF))
        self.nodes.append(SubstructNode(SubstructNodeType.ACCESS))

    def add_access(self):
        self.nodes.append(SubstructNode(SubstructNodeType.ACCESS))

    def add_index(self, idx):
        self.nodes.append(SubstructNode(SubstructNodeType.INDEX, idx))
    
    def add_deref(self):
        self.nodes.append(SubstructNode(SubstructNodeType.DEREF))
    
    def build(self):
        return deque(self.nodes)
