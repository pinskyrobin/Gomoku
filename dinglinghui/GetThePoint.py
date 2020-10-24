"""
import logging
from la.evaluate import BoardEvaluate
from dinglinghui.Macro import BLANK, WIDTH, DEPTH, HEIGHT, WHITE
from dinglinghui.Node import Node


def search_line(board, row):
    # TODO:This is function isn't work well.
    node_list = []
    for i in range(1, WIDTH, 2):
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


def evaluate_point(board, player):
    evalue = BoardEvaluate(board, player)
    return evalue.evaluate()


def create_nodes(board, node, node_list, alpha, beta, max_value, min_value, player):
    logging.debug("enter create nodes function")
    logging.info("alpha: " + str(alpha))
    # well, i can input chinese on my computer.
    # player is refer to the one who is player, possibly is the one chess. not player is the opponent
    if node.depth <= DEPTH & node.kind == player:
        node.create_children(search_node(board, node_list))
        for i in node.children:
            node_list.append(i)
            i.beta = evaluate_point(board, player)
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
            node_list.append(i)
            i.alpha = evaluate_point(board, player)
            restore_board(board, node_list)
            alpha += i.alpha
            if alpha > max_value:
                create_nodes(board, i, node_list, alpha, beta, alpha, min_value, not player)
            else:
                node_list.pop()


def create_and_pure_tree(board, player):
    logging.debug("enter create and pure the tree function")
    logging.info("player: " + str(player))
    node = Node(0, 0)
    node.kind = WHITE
    nodes = [node]
    create_nodes(board, node, nodes, 0, 0, 0, 1000, player)
    return nodes[0].x, nodes[0].y
"""
import time

from dinglinghui.Macro import HEIGHT, WIDTH, SCORE_MIN, SCORE_MAX, SCORE_FIVE, MAP_ENTRY_TYPE, DEPTH, BLANK
from la.evaluate import BoardEvaluate


def isWin(board, turn):
    boardevaluate = BoardEvaluate(board, turn)
    return boardevaluate.evaluate()


# get all positions that is empty
def genmove(board):
    moves = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board.board[y][x] == BLANK:
                score = board.pos_score[y][x]
                moves.append((score, x, y))

    moves.sort(reverse=True)
    return moves


def search(board, turn):
    moves = genmove(board)
    boardevaluate = BoardEvaluate(board, turn)
    bestmove = None
    max_score = -0x7fffffff
    for score, x, y in moves:
        board.board[y][x] = turn
        score = boardevaluate.evaluate()
        board.board[y][x] = 0

        if score > max_score:
            max_score = score
            bestmove = (max_score, x, y)
    return bestmove


def findBestChess(board, turn):
    time1 = time.time()
    score, x, y = search(board, turn)
    time2 = time.time()
    print('time[%f] (%d, %d), score[%d] save[%d]' % ((time2 - time1), x, y, score, turn))
    return x, y


# check if has a none empty position in it's radius range
def hasNeighbor(board, x, y, radius):
    start_x, end_x = (x - radius), (x + radius)
    start_y, end_y = (y - radius), (y + radius)

    for i in range(start_y, end_y + 1):
        for j in range(start_x, end_x + 1):
            if 0 <= i < HEIGHT and 0 <= j < WIDTH:
                if board[i][j] != 0:
                    return True
    return False


def __search(board, turn, depth, alpha=SCORE_MIN, beta=SCORE_MAX):
    boardevaluate = BoardEvaluate(board, turn)
    score = boardevaluate.evaluate()
    if depth <= 0 or abs(score) >= SCORE_FIVE:
        return score

    moves = genmove(board)
    bestmove = None
    board.alpha += len(moves)

    # if there are no moves, just return the score
    if len(moves) == 0:
        return score

    for _, x, y in moves:
        board.board[y][x] = turn

        if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_TWO
        else:
            op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_ONE

        score = __search(board, op_turn, depth - 1, -beta, -alpha)

        board.board[y][x] = 0
        board.beta += 1

        # alpha/beta pruning
        if score > alpha:
            alpha = score
            bestmove = (x, y)
            if alpha >= beta:
                break

    if depth == DEPTH and bestmove:
        board.bestmove = bestmove

    return alpha
