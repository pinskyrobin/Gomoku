import sys

from PyQt5.QtWidgets import QApplication

from window import GomokuWindow

app = QApplication(sys.argv)
ex = GomokuWindow()
sys.exit(app.exec_())

