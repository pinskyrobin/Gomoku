
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = []
        self.depth = 0

    def create_children(self, node_list):
        self.children = node_list[:]
