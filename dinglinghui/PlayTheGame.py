from Board import Board
from GetThePoint import create_tree, find_the_best
from Macro import FIRST_POINT, PLAY_MODE, PLAY_STATUS


def update_board(board, x, y, kind):
    board.chessboard[y][x] = kind
    return x, y, kind


def human_play(self, board):
    if board.hands == 0:
        return first_play(self, board)
    x, y = input("input position:")
    update_board(board, x, y, which_color(self, board))
    board.hands += 1
    return x, y


def first_play(self, board):
    x, y = board.first_play(FIRST_POINT.KIND_2)
    board.chessboard[y][x] = self.first
    update_board(board, x, y, self.first)
    board.hands += 1
    return x, y


def which_color(self, board):
    if board.hands % 2 == 0:
        return self.first
    else:
        return not self.first


def machine_play(self, board):
    if board.hands == 0:
        first_play(self, board)
    else:
        node = create_tree(board)
        result = find_the_best(node)
        update_board(board, result.x, result.y, which_color(self, board))
    board.hands += 1


def play_game(status, mode):
    board = Board()
    while status == PLAY_STATUS.NOT_SURE:
        if mode == PLAY_MODE.MACHINE_MACHINE:
            machine_play(status, board)
            machine_play(status, board)
        elif mode == PLAY_MODE.MACHINE_HUMAN:
            machine_play(status, board)
            human_play(status, board)
        else:
            human_play(status, board)
            machine_play(status, board)
        status = board.judge_status()
    print(status)
    exit(0)
