import os, sys
import traceback
from patest import Gamsain
from sectors import sectors
from add import add
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import pandas as pd

# 경로 지정?
root = os.path.dirname(os.path.abspath(__file__))
MainUI = uic.loadUiType(os.path.join(root, 'main.ui'))[0]


class MainDialog(QMainWindow, MainUI):
    try:
        def __init__(self):
            super().__init__()
            self.setupUi(self)  # This must come before any usage of UI elements
            self.setWindowTitle('Main')
            self.sector = sectors()
            self.secAllBtn.clicked.connect(lambda: self.sector.secAllBtn_clicked(self))
            self.secAllBtn.clicked.connect(lambda: self.sector.secReadyBtn_clicked(self))
            self.secAllBtn.clicked.connect(lambda: self.sector.secFailBtn_clicked(self))
            self.secAllBtn.clicked.connect(lambda: self.sector.secOkBtn_clicked(self))

            self.add = add()
            self.add.btn(self)

            self.gamasain_instance = Gamsain()
            df = pd.read_csv("IPO현황_최종.csv", encoding="cp949")
            self.gamasain_instance.create_gamsain_chart(self, df['주선인'])



    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())




