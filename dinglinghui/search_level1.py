import time
from enum import IntEnum
from la.evaluate import BoardEvaluate
from dinglinghui.Macro import MAP_ENTRY_TYPE, CHESS_TYPE
from dinglinghui.GameMap import *



CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value


class ChessAI():
    def __init__(self, chess_len):
        self.save_count = 0
        self.len = chess_len
        # [horizon, vertical, left diagonal, right diagonal]
        self.record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]
        self.pos_score = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(chess_len)] for y in range(chess_len)]

    def reset(self):
        for y in range(self.len):
            for x in range(self.len):
                for i in range(4):
                    self.record[y][x][i] = 0

        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0

    def isWin(self, board, turn):
        board_evaluate = BoardEvaluate(board, turn)
        return board_evaluate.evaluate()

    # get all positions that is empty
    def genmove(self, board):
        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if board[x][y] == 0:
                    score = self.pos_score[y][x]
                    moves.append((score, x, y))
                else:
                    print("board [%d] [%d] is not empty", x, y)

        moves.sort(reverse=True)
        return moves

    def search(self, board, turn):
        moves = self.genmove(board)
        board_evaluate = BoardEvaluate(board, turn)
        bestmove = None
        max_score = -0x7fffffff
        for score, x, y in moves:
            board[x][y] = turn.value
            score = board_evaluate.evaluate()
            board[x][y] = 0

            if score > max_score:
                max_score = score
                bestmove = (max_score, x, y)
        return bestmove

    def findBestChess(self, board, turn):
        time1 = time.time()
        score, x, y = self.search(board, turn)
        time2 = time.time()
        # print('time[%f] (%d, %d), score[%d] save[%d]' % ((time2 - time1), x, y, score, self.save_count))
        print('time[%f] (%d, %d), score[%d]' % ((time2 - time1), x, y, score))
        return x, y
