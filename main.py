from PyQt5.QtWidgets import QApplication
from game import Gomoku
from window import GomokuWindow
import sys


app = QApplication(sys.argv)
ex = GomokuWindow()
ex.show()
sys.exit(app.exec_())


