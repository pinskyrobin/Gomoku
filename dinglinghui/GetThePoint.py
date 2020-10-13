from .Macro import BOARD_BUILTIN, PLAYER
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


def update_board(board, node_list):
    for i in node_list:
        board.chessboard[i.y][i.x] = i.kind
    return board


def restore_board(board, node_list):
    for i in node_list:
        board.chessboard[i.y][i.x] = BOARD_BUILTIN.BLANK


def search_node(board, node_list):
    nodes = []
    board = update_board(board, node_list)
    for i in range(BOARD_BUILTIN.HEIGHT):
        nodes.extend(search_line(board, i))
    restore_board(board, node_list)
    return nodes


def evaluate_point(board):
    return 1


def create_nodes(board, node, node_list, alpha, beta, max_value, min_value, player):
    # well, i can input chinese on my computer.
    # player is refer to the one who is player, possibly is the one chess. not player is the opponent
    if node.depth <= BOARD_BUILTIN.DEPTH & node.kind == player:
        node.create_children(search_node(board, node_list))
        for i in node.children:
            node_list.append(node)
            i.beta = evaluate_point(update_board(board, node_list))
            restore_board(board, node_list)
            beta += i.beta
            if beta < min_value:
                i.beta = beta
                # sign to show this node is runnable
                create_nodes(board, i, node_list, alpha, beta, max_value, beta, not player)
            else:
                node_list.pop()
    elif node.depth <= BOARD_BUILTIN.DEPTH & node.kind != player:
        node.create_children(search_node(board, node_list))
        for i in node.children:
            node_list.append(node)
            i.alpha = evaluate_point(update_board(board, node_list))
            restore_board(board, node_list)
            alpha += i.value
            if alpha > max_value:
                create_nodes(board, i, node_list, alpha, beta, alpha, min_value, not player)
            else:
                node_list.pop()
    else:
        return node_list


def create_and_pure_tree(board):
    node = Node(-1, -1)
    nodelist = create_nodes(board, node, [], 0, 0, 0, 1000, 1)
    return nodelist[0]


