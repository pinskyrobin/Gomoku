from Board import Board
from Macro import PLAY_MODE, PLAY_STATUS, BOARD_BUILTIN
from PlayTheGame import human_play, machine_play


class play:
    def __init__(self, play_mode, hardship):
        self.status = PLAY_STATUS.NOT_SURE
        self.play_mode = play_mode
        self.hardship = hardship
        self.first = BOARD_BUILTIN.BLACK
