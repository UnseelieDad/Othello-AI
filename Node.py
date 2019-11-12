# Node class for use with trees and minimax
class Node:

    # Node has data (boardState), a heuristic, children, a parent, and a move associated with it
    def __init__(self, data, move):
        self.data = data
        self.heuristic = None
        self.children = []
        self.parent = None
        self.move = move

    def addChild(self, node):
        node.parent = self    
        self.children.append(node)