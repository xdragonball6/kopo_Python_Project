import os, sys
import traceback

from add import add
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


# 경로 지정?
root = os.path.dirname(os.path.abspath(__file__))
MainUI = uic.loadUiType(os.path.join(root, 'main.ui'))[0]


class MainDialog(QMainWindow, MainUI):
    try:
        def __init__(self):
            super().__init__()
            self.setupUi(self)  # This must come before any usage of UI elements
            self.setWindowTitle('Main')
            self.add = add()

            self.add.btn(self)



    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())




