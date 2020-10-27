import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QDesktopWidget, QMessageBox
from MainWindow import GomokuWindow
from StartWindow import Ui_Form


class RunStart(QWidget, Ui_Form):
    def __init__(self):
        super(RunStart, self).__init__()
        self.setupUi(self)


def StartPlay():
    startWindow.hide()
    ex.show()


app = QApplication(sys.argv)
startWindow = RunStart()
ex = GomokuWindow()
startWindow.show()
startWindow.StartButton.clicked.connect(StartPlay)


sys.exit(app.exec_())

