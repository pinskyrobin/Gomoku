import random
import time
from enum import IntEnum
from random import sample

from dinglinghui.Macro import MAP_ENTRY_TYPE, CHESS_TYPE, HEIGHT, WIDTH
from la.evaluate import BoardEvaluate

AI_SEARCH_DEPTH = 2

CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value

SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX
SCORE_FIVE = 10000





class ChessAI():
    def __init__(self, chess_len):
        self.len = chess_len
        # [horizon, vertical, left diagonal, right diagonal]
        self.record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
        self.pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(chess_len)] for y in range(chess_len)]


    def isWin(self, board, turn):
        board_evaluate = BoardEvaluate(board, turn)
        return board_evaluate.evaluate()

    # check if has a none empty position in it's radius range
    def hasNeighbor(self, board, x, y, radius):
        start_x, end_x = (x - radius), (x + radius)
        start_y, end_y = (y - radius), (y + radius)

        for i in range(start_y, end_y + 1):
            for j in range(start_x, end_x + 1):
                if 0 <= i < self.len and 0 <= j < self.len:
                    if board[i][j] != 0:
                        return True
        return False

    # get all positions near chess
    def genmove(self, board, turn):
        moves = []
        radius = 1

        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0 and self.hasNeighbor(board, x, y, radius):
                    score = self.pos_score[y][x]
                    moves.append((score, x, y))

        moves.sort(reverse=True)

        return moves

    def __search(self, board, turn, depth, alpha=SCORE_MIN, beta=SCORE_MAX):
        board_evaluate = BoardEvaluate(board, turn)
        score = board_evaluate.evaluate()
        if depth <= 0 or abs(score) >= SCORE_FIVE:
            return score

        moves = self.genmove(board, turn)
        bestmove = None
        self.alpha += len(moves)

        # if there are no moves, just return the score
        if len(moves) == 0:
            return score

        for _, x, y in moves:
            board[y][x] = turn

            if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_TWO
            else:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_ONE

            score = - self.__search(board, op_turn, depth - 1, -beta, -alpha)

            board[y][x] = 0
            self.belta += 1

            # alpha/beta pruning
            if score > alpha:
                alpha = score
                bestmove = (x, y)
                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        return alpha

    def search(self, board, turn, depth=4):
        self.maxdepth = depth
        self.bestmove = None
        moves = []
        score = self.__search(board, turn, depth)
        if self.bestmove:
            x, y = self.bestmove
            return score, x, y
        else:
            for i in range(self.len):
                for j in range(self.len):
                    if board[i][j] == 0:
                        score = self.pos_score[i][j]
                        moves.append((score, i, j))
            k = len(moves)
            res = random.randint(0, k - 1)
            return moves[res]


    def findBestChess(self, board, turn):
        time1 = time.time()
        self.alpha = 0
        self.belta = 0
        insult = turn
        score, x, y = self.search(board, turn, AI_SEARCH_DEPTH)
        time2 = time.time()
        print('time[%.2f] (%d, %d, %d), score[%d] alpha[%d] belta[%d]' % (
            (time2 - time1), x, y, insult, score, self.alpha, self.belta))
        return x, y
