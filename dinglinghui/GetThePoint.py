from .Macro import BOARD_BUILTIN
from .Node import Node


def search_line(board, row):
    node_list = []
    for i in range(2, BOARD_BUILTIN.WIDTH, 2):
        if board.chessboard[row][i] != BOARD_BUILTIN.BLANK:
            if board.chessboard[row][i - 1] == BOARD_BUILTIN.BLANK:
                node = Node(i - 1, row)
                node_list.append(node)
            if board.chessboard[row][i - 2] == BOARD_BUILTIN.BLANK:
                node = Node(i - 2, row)
                node_list.append(node)
    return node_list


def search_node(board, node_list):
    node_list = []
    board.chessboard[node.y][node.x] = BOARD_BUILTIN.BLACK
    for i in range(BOARD_BUILTIN.HEIGHT):
        node_list.extend(search_line(board, i))

    return node_list


def create_nodes(board, node):
    if node.depth <= BOARD_BUILTIN.DEPTH:
        node.create_children(search_node(board, node))
        for i in node.children:
            create_nodes(board, i)



def create_tree(board):
    node = Node(-1, -1)
    create_nodes(board, node)
    return node


def traverse_tree(node):
    for i in node.children:
        print("This is a node's x: " + i.x)
        traverse_tree(i)


def find_the_best(node):
    return node
