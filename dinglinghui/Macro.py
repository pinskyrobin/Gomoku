from enum import IntEnum


class PLAY_STATUS(IntEnum):
    TIE = 0
    BLACK_WIN = 1
    WHITE_WIN = -1
    NOT_SURE = 2


class PLAY_MODE(IntEnum):
    MACHINE_MACHINE = 0
    MACHINE_HUMAN = 1
    HUMAN_MACHINE = -1


class OPPONENT_LEVEL(IntEnum):
    HARD = 1
    NORMAL = 0
    EASY = -1


class PLAYER(IntEnum):
    MACHINE = 1
    HUMAN = 0
    OPPONENT_MACHINE = -1


class FIRST_POINT(IntEnum):
    KIND_1 = 1
    KIND_2 = 2


class BOARD_BUILTIN(IntEnum):
    WIDTH = 15,
    HEIGHT = 15,
    BLACK = 1,
    WHITE = -1,
    BLANK = 0,
    DEPTH = 4,


class WINDOW(IntEnum):
    REC_SIZE = 50
    CHESS_RADIUS = REC_SIZE // 2 - 2
    CHESS_LEN = 15
    MAP_WIDTH = CHESS_LEN * REC_SIZE
    MAP_HEIGHT = CHESS_LEN * REC_SIZE

    INFO_WIDTH = 200
    BUTTON_WIDTH = 140
    BUTTON_HEIGHT = 50

    SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH
    SCREEN_HEIGHT = MAP_HEIGHT
