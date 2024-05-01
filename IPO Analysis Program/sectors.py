import traceback

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAbstractItemView

from sec import main as m
import sec

class sectors:
    count = 0
    def secAllBtn_clicked(self, dialog):
        self.count = 1
        sec.create_chart(m.df, m.success_df, m.ing_df, m.fail_df, self.count)
        m.summary(self, dialog, m.total_df_file)
        dialog.secTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pixmap = QPixmap('전체업종.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secReadyBtn_clicked(self, dialog):
        self.count = 2
        sec.create_chart(m.df, m.success_df, m.ing_df, m.fail_df, self.count)
        m.summary(self, dialog, m.ing_df_file)
        dialog.secTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pixmap = QPixmap('심사중.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secFailBtn_clicked(self, dialog):
        self.count = 3
        sec.create_chart(m.df, m.success_df, m.ing_df, m.fail_df, self.count)
        m.summary(self, dialog, m.fail_df_file)
        dialog.secTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pixmap = QPixmap('심사실패.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secOkBtn_clicked(self, dialog):
        self.count = 4
        sec.create_chart(m.df, m.success_df, m.ing_df, m.fail_df, self.count)
        m.summary(self, dialog, m.success_df_file)
        dialog.secTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pixmap = QPixmap('심사성공.png')
        dialog.label_chart.setPixmap(pixmap)
        dialog.label_chart.show()

    def secDown_clicked(self):
        if self.count == 1:
            m.total_df_file.to_excel('./IPO 신청 전체 기업 수 데이터_업종별.xlsx')
        elif self.count == 2:
            m.ing_df_file.to_excel('./IPO 승인 대기 기업 수 데이터_업종별.xlsx')
        elif self.count == 3:
            m.fail_df_file.to_excel('./IPO 실패 기업 수 데이터_업종별.xlsx')
        elif self.count == 4:
            m.success_df_file.to_excel('./IPO 승인 완료 기업 수 데이터_업종별.xlsx')