"""
from dinglinghui.GetThePoint import create_and_pure_tree
import logging

from dinglinghui.Macro import KIND_2


def update_board(board, x, y, kind):
    board.chessboard[y][x] = kind
    return x, y, kind


def human_play(player, board, x, y):
    logging.debug("enter human play function")
    logging.info("player: "+str(player))
    if board.hands == 0:
        return first_play(player, board)
    # x, y = input("input position:")
    update_board(board, x, y, player)
    board.hands += 1
    return board


def first_play(player, board):
    logging.debug("enter first play function")
    logging.info("player: "+str(player))
    board.chessboard[7][7] = player
    update_board(board, 7, 7, player)
    board.hands += 1
    return board


def machine_play(player, board):
    logging.debug("enter machine play function")
    logging.info("This is the player: "+str(player))
    x, y = 0, 0
    if board.hands == 0:
        x, y = first_play(player, board)
    else:
        x, y = create_and_pure_tree(board, player)
        # update_board(board, result.x, result.y, player)
    board.hands += 1
    return x, y
"""

