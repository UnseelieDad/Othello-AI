class Node:

    def __init__(self, data):
        self.data = data
        self.heuristic = None
        self.children = []
        self.parent = None
        self.alpha = None
        self.beta = None

    def addChild(self, node):
        node.parent = self
        self.children.append(node)

    def getParent(self):
        return self.parent