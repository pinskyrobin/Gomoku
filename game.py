from dinglinghui.Board import Board
from dinglinghui.Macro import BLACK, HEIGHT, WIDTH, WHITE, BLANK
from dinglinghui.PlayTheGame import machine_play


class Gomoku:

    def __init__(self):
        self.g_map = [[0 for y in range(15)] for x in range(15)]  # 当前的棋盘
        self.cur_step = 0  # 步数
        self.max_search_steps = 3  # 最远搜索2回合之后

    def move_1step(self, pos_x=None, pos_y=None):
        """
        玩家落子
        :param pos_x: 输入的x坐标
        :param pos_y: 输入的y坐标
        """
        while True:
            # TODO: 加入AI后，需要把内嵌if语句删掉
            board = Board()
            board.hands = 0
            update_board(self, pos_x, pos_y, board)
            transfer_list2_board_chess(self, board)
            pos_x, pos_y = machine_play(BLACK, board)
            update_board(self, pos_x, pos_y, board)
            return

    def game_result(self, show=False):
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(11):
            for y in range(15):
                if self.g_map[x][y] == 1 and \
                        self.g_map[x + 1][y] == 1 and \
                        self.g_map[x + 2][y] == 1 and \
                        self.g_map[x + 3][y] == 1 and \
                        self.g_map[x + 4][y] == 1:
                    if show:
                        return 1, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and \
                        self.g_map[x + 1][y] == 2 and \
                        self.g_map[x + 2][y] == 2 and \
                        self.g_map[x + 3][y] == 2 and \
                        self.g_map[x + 4][y] == 2:
                    if show:
                        return 2, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 2

        # 2. 判断是否纵向连续五子
        for x in range(15):
            for y in range(11):
                if self.g_map[x][y] == 1 and \
                        self.g_map[x][y + 1] == 1 and \
                        self.g_map[x][y + 2] == 1 and \
                        self.g_map[x][y + 3] == 1 and \
                        self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and \
                        self.g_map[x][y + 1] == 2 and \
                        self.g_map[x][y + 2] == 2 and \
                        self.g_map[x][y + 3] == 2 and \
                        self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 2

        # 3. 判断是否有左上-右下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and \
                        self.g_map[x + 1][y + 1] == 1 and \
                        self.g_map[x + 2][y + 2] == 1 and \
                        self.g_map[x + 3][y + 3] == 1 and \
                        self.g_map[x + 4][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x][y] == 2 and \
                        self.g_map[x + 1][y + 1] == 2 and \
                        self.g_map[x + 2][y + 2] == 2 and \
                        self.g_map[x + 3][y + 3] == 2 and \
                        self.g_map[x + 4][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + t) for t in range(5)]
                    else:
                        return 2

        # 4. 判断是否有右上-左下的连续五子
        for x in range(11):
            for y in range(11):
                if self.g_map[x + 4][y] == 1 and \
                        self.g_map[x + 3][y + 1] == 1 and \
                        self.g_map[x + 2][y + 2] == 1 and \
                        self.g_map[x + 1][y + 3] == 1 and \
                        self.g_map[x][y + 4] == 1:
                    if show:
                        return 1, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 1
                if self.g_map[x + 4][y] == 2 and \
                        self.g_map[x + 3][y + 1] == 2 and \
                        self.g_map[x + 2][y + 2] == 2 and \
                        self.g_map[x + 1][y + 3] == 2 and \
                        self.g_map[x][y + 4] == 2:
                    if show:
                        return 2, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 2

        # 5. 判断是否为平局
        for x in range(15):
            for y in range(15):
                if self.g_map[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    if show:
                        return 0, [(-1, -1)]
                    else:
                        return 0

        if show:
            return 3, [(-1, -1)]
        else:
            return 3


def update_board(self, pos_x, pos_y, board):
    if 0 <= pos_x <= 14:
        if 0 <= pos_y <= 14:
            if self.g_map[pos_x][pos_y] == 0:
                if self.cur_step % 2 == 0:
                    self.g_map[pos_x][pos_y] = 1
                else:
                    self.g_map[pos_x][pos_y] = 2
            self.cur_step += 1
            board.hands += 1


def transfer_list2_board_chess(self, board):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if self.g_map[i][j] == 1:
                board.chessboard[i][j] = BLACK
            elif self.g_map[i][j] == 2:
                board.chessboard[i][j] = WHITE
            else:
                board.chessboard[i][j] = BLANK


