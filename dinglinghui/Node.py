from .Macro import BOARD_BUILTIN

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = []
        self.depth = 0
        self.kind = BOARD_BUILTIN.BLANK
        self.alpha = 1000
        self.beta = -1000

    def create_children(self, node_list):
        self.children = node_list[:]
