from random import randint

from .Macro import BLACK, WIDTH, HEIGHT, WHITE_WIN, BLACK_WIN, KIND_1, NOT_SURE, BLANK


class Board:
    def __init__(self):
        self.board = [[BLANK for y in range(15)] for x in range(15)]
        self.alpha = 0
        self.beta = 0
        self.bestmove = None
        self.pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(HEIGHT)] for y in range(WIDTH)]

