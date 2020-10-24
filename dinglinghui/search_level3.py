import random
import time
from enum import IntEnum

from dinglinghui.Macro import MAP_ENTRY_TYPE, CHESS_TYPE, HEIGHT, WIDTH
from la.evaluate import BoardEvaluate

AI_SEARCH_DEPTH = 4
AI_LIMITED_MOVE_NUM = 20




CHESS_TYPE_NUM = 8

FIVE = CHESS_TYPE.LIVE_FIVE.value
FOUR, THREE, TWO = CHESS_TYPE.LIVE_FOUR.value, CHESS_TYPE.LIVE_THREE.value, CHESS_TYPE.LIVE_TWO.value
SFOUR, STHREE, STWO = CHESS_TYPE.CHONG_FOUR.value, CHESS_TYPE.SLEEP_THREE.value, CHESS_TYPE.SLEEP_TWO.value

SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX
SCORE_FIVE, SCORE_FOUR, SCORE_SFOUR = 100000, 10000, 1000
SCORE_THREE, SCORE_STHREE, SCORE_TWO, SCORE_STWO = 100, 10, 8, 2


class ChessAI():
    def __init__(self, chess_len):
        self.len = chess_len
        # [horizon, vertical, left diagonal, right diagonal]
        self.record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
        self.count = [[0 for x in range(CHESS_TYPE_NUM)] for i in range(2)]

    def reset(self):
        for y in range(self.len):
            for x in range(self.len):
                for i in range(4):
                    self.record[y][x][i] = 0

        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0

    def click(self, map, x, y, turn):
        map.click(x, y, turn)

    def isWin(self, board, turn):
        board_evaluate = BoardEvaluate(board, turn)
        return board_evaluate.evaluate()

    # evaluate score of point, to improve pruning efficiency
    def evaluatePointScore(self, board, x, y, mine, opponent):
        board_evaluate = BoardEvaluate(board, turn)
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]  # direction from left to right
        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0

        board[y][x] = mine
        board_evaluate.evaluatePoint_level3(x, y, mine, opponent, self.count[opponent-1])
        mine_count = self.count[mine - 1]
        board[y][x] = opponent
        board_evaluate.evaluatePoint_level3(x, y, opponent, mine, self.count[mine-1])
        opponent_count = self.count[opponent - 1]
        board[y][x] = 0

        mscore = board_evaluate.getPointScore(mine_count)
        oscore = board_evaluate.getPointScore(opponent_count)

        return (mscore, oscore)

    # check if has a none empty position in it's radius range
    def hasNeighbor(self, board, x, y, radius):
        start_x, end_x = (x - radius), (x + radius)
        start_y, end_y = (y - radius), (y + radius)

        for i in range(start_y, end_y + 1):
            for j in range(start_x, end_x + 1):
                if i >= 0 and i < self.len and j >= 0 and j < self.len:
                    if board[i][j] != 0:
                        return True
        return False

    # get all positions near chess
    def genmove(self, board, turn):
        board_evaluate = BoardEvaluate(board, turn)
        fives = []
        mfours, ofours = [], []
        msfours, osfours = [], []
        mine,opponent = 0, 0
        if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            mine = 1
            opponent = 2
        else:
            mine = 2
            opponent = 1

        moves = []
        radius = 1

        for y in range(self.len):
            for x in range(self.len):
                if board[x][y] == 0 and self.hasNeighbor(board, x, y, radius):
                    mscore, oscore = board_evaluate.evaluatePointScore(x, y, mine, opponent)
                    point = (max(mscore, oscore), x, y)

                    if mscore >= SCORE_FIVE or oscore >= SCORE_FIVE:
                        fives.append(point)
                    elif mscore >= SCORE_FOUR:
                        mfours.append(point)
                    elif oscore >= SCORE_FOUR:
                        ofours.append(point)
                    elif mscore >= SCORE_SFOUR:
                        msfours.append(point)
                    elif oscore >= SCORE_SFOUR:
                        osfours.append(point)

                    moves.append(point)

        if len(fives) > 0: return fives

        if len(mfours) > 0: return mfours

        if len(ofours) > 0:
            if len(msfours) == 0:
                return ofours
            else:
                return ofours + msfours

        moves.sort(reverse=True)

        # FIXME: decrease think time: only consider limited moves with higher scores
        if self.maxdepth > 2 and len(moves) > AI_LIMITED_MOVE_NUM:
            moves = moves[:AI_LIMITED_MOVE_NUM]
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
            board[x][y] = turn

            if turn == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_TWO
            else:
                op_turn = MAP_ENTRY_TYPE.MAP_PLAYER_ONE

            score = - self.__search(board, op_turn, depth - 1, -beta, -alpha)

            board[x][y] = 0
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
        score = self.__search(board, turn, depth)
        if self.bestmove != None:
            x, y = self.bestmove
            return score, x, y
        else:
            moves = []
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (board[i][j] == 0):
                        moves.append((score, i, j))
            k = len(moves)
            res = random.randint(0, k - 1)
            return moves[res]

    def findBestChess(self, board, turn):
        time1 = time.time()
        self.alpha = 0
        self.belta = 0
        score, x, y = self.search(board, turn, AI_SEARCH_DEPTH)
        time2 = time.time()
        print('time[%.2f] (%d, %d), score[%d] alpha[%d] belta[%d]' % (
        (time2 - time1), x, y, score, self.alpha, self.belta))
        return (x, y)
