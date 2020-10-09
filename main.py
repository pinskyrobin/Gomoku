from PyQt5.QtWidgets import QApplication
from game import Gomoku
from window import GomokuWindow
import sys


app = QApplication(sys.argv)
ex = GomokuWindow()
sys.exit(app.exec_())


