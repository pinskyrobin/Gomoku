from random import randint

import numpy as np

from .Macro import PLAY_STATUS, FIRST_POINT, BOARD_BUILTIN


class Board:
    def __init__(self):
        y, x = BOARD_BUILTIN.HEIGHT, BOARD_BUILTIN.WIDTH
        scale = (y, x)
        self.chessboard = np.zeros(scale)
        self.hands = 0
        pass

    def judge_status(self):
        if self.chessboard[0][0] == BOARD_BUILTIN.BLACK:
            return PLAY_STATUS.BLACK_WIN
        else:
            return PLAY_STATUS.WHITE_WIN
        pass

    def first_play(self, first_point_demand):
        if self.hands != 0:
            print("Not the First to play")
        if first_point_demand == FIRST_POINT.KIND_1:
            return randint(4, BOARD_BUILTIN.WIDTH - 4), randint(4, BOARD_BUILTIN.HEIGHT - 4)
        else:
            return 7, 7
