import os, sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

# 경로 지정?
root = os.path.dirname(os.path.abspath(__file__))
MainUI = uic.loadUiType(os.path.join(root, 'main.ui'))[0]


class MainDialog(QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('main')

        self.addMap()


    def addMap(self):
        self.map1.setStyleSheet('border-image: url(./map1.png)')
        self.map2.setStyleSheet('border-image: url(./map2.png)')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())



