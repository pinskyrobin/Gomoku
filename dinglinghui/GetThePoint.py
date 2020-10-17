import logging

from dinglinghui.Macro import BLANK, WIDTH, DEPTH, HEIGHT
from dinglinghui.Node import Node


def search_line(board, row):
    node_list = []
    for i in range(2, WIDTH, 2):
        if board.chessboard[row][i] != BLANK:
            if board.chessboard[row][i - 1] == BLANK:
                node = Node(i - 1, row)
                node_list.append(node)
            if board.chessboard[row][i - 2] == BLANK:
                node = Node(i - 2, row)
                node_list.append(node)
    return node_list


def update_board(board, node_list):
    for i in node_list:
        board.chessboard[i.y][i.x] = i.kind
    return board


def restore_board(board, node_list):
    for i in node_list:
        board.chessboard[i.y][i.x] = BLANK


def search_node(board, node_list):
    nodes = []
    board = update_board(board, node_list)
    for i in range(HEIGHT):
        nodes.extend(search_line(board, i))
    restore_board(board, node_list)
    return nodes


def evaluate_point():
    return 1


def create_nodes(board, node, node_list, alpha, beta, max_value, min_value, player):
    logging.debug("enter create nodes function")
    logging.info("alpha: " + str(alpha))
    # well, i can input chinese on my computer.
    # player is refer to the one who is player, possibly is the one chess. not player is the opponent
    if node.depth <= DEPTH & node.kind == player:
        node.create_children(search_node(board, node_list))
        for i in node.children:
            node_list.append(node)
            i.beta = evaluate_point()
            restore_board(board, node_list)
            beta += i.beta
            if beta < min_value:
                i.beta = beta
                # sign to show this node is runnable
                create_nodes(board, i, node_list, alpha, beta, max_value, beta, not player)
            else:
                node_list.pop()
    elif node.depth <= DEPTH & node.kind != player:
        node.create_children(search_node(board, node_list))
        for i in node.children:
            node_list.append(node)
            i.alpha = evaluate_point()
            restore_board(board, node_list)
            alpha += i.alpha
            if alpha > max_value:
                create_nodes(board, i, node_list, alpha, beta, alpha, min_value, not player)
            else:
                node_list.pop()


def create_and_pure_tree(board, player):
    logging.debug("enter create and pure the tree function")
    logging.info("player: " + str(player))
    node = Node(1, 1)
    nodes = [node]
    create_nodes(board, node, nodes, 0, 0, 0, 1000, player)
    return nodes[0].x, nodes[0].y
