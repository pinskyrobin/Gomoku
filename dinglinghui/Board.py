from random import randint

from .Macro import BLACK, WIDTH, HEIGHT, WHITE_WIN, BLACK_WIN, KIND_1


class Board:
    def __init__(self):
        self.chessboard = [[0 for y in range(15)] for x in range(15)]
        self.hands = 0
        pass

    def judge_status(self):
        if self.chessboard[0][0] == BLACK:
            return BLACK_WIN
        else:
            return WHITE_WIN
        pass

    def first_play(self, first_point_demand):
        if self.hands != 0:
            print("Not the First to play")
        if first_point_demand == KIND_1:
            return randint(4, WIDTH - 4), randint(4, HEIGHT - 4)
        else:
            return 7, 7
