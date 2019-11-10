class Node:

    def __init__(self, data, name):
        self.data = data
        self.heuristic = None
        self.children = []
        self.parent = None
        self.name = name

    def addChild(self, node):
        node.parent = self    
        self.children.append(node)