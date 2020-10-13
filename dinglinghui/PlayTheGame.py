from .Board import Board
from .GetThePoint import create_and_pure_tree
from .Macro import FIRST_POINT, PLAY_MODE, PLAY_STATUS, BOARD_BUILTIN


def update_board(board, x, y, kind):
    board.chessboard[y][x] = kind
    return x, y, kind


def human_play(player, board, x, y):
    if board.hands == 0:
        return first_play(player, board)
    # x, y = input("input position:")
    update_board(board, x, y, player)
    board.hands += 1
    return board


def first_play(player, board):
    x, y = board.first_play(FIRST_POINT.KIND_2)
    board.chessboard[y][x] = player
    update_board(board, x, y, player)
    board.hands += 1
    return x, y


def machine_play(player, board):
    if board.hands == 0:
        first_play(player, board)
    else:
        result = create_and_pure_tree(board, player)
        update_board(board, result.x, result.y, player)
    board.hands += 1
    return board


