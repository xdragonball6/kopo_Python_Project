from PyQt5.QtGui import QPixmap

class sectors:
    def secAllBtn_clicked(self, dialog):
        pixmap = QPixmap('total.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secReadyBtn_clicked(self, dialog):
        pixmap = QPixmap('ing.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secFailBtn_clicked(self, dialog):
        pixmap = QPixmap('fail.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secOkBtn_clicked(self, dialog):
        pixmap = QPixmap('success.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()