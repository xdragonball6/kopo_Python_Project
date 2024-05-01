import os, sys
import traceback

import pandas as pd
import plotly.graph_objects as go
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

# Test 클래스 정의
class Gamsain:
    df3 = pd.Series()
    df4 = pd.DataFrame()
    num = 0
    def process_column(self, column_series):
        if column_series.str.contains(',').any():
            processed_values = column_series.str.split(',')
            return processed_values.explode()
        else:
            return column_series
#====================전체 조회=============================================================
    def create_gamsain_chart(self, dialog, column_series, threshold=0.01):
        try:
            df = column_series.str.split(',')
            exploded_df = df.explode()
            counts = exploded_df.value_counts()
            self.df3 = counts
            processed_column = self.process_column(column_series)
            value_counts = processed_column.value_counts()
            total_count = value_counts.sum()
            filtered_counts = value_counts[value_counts / total_count >= threshold]
            etc_count = value_counts[value_counts / total_count < threshold].sum()
            filtered_counts['etc'] = etc_count
            fig = go.Figure(data=[go.Pie(labels=filtered_counts.index, values=filtered_counts.values)])
            fig.update_layout(title='상장 주선인')
            fig.write_html("감사인.html")
            html_path = os.path.abspath("감사인.html")
            dialog.gamsain_webEngineView.setUrl(QUrl.fromLocalFile(html_path))
            exeldf = self.df3.to_frame(name='성공횟수')
            exeldf.reset_index(inplace=True)
            exeldf.rename(columns={'index': '회사', '성공횟수': '건수'}, inplace=True)
            self.df4 = exeldf
            tableHeader = ['주선인', '건수']
            # print(len(df))
            dialog.paTable.setRowCount(len(exeldf))
            dialog.paTable.setColumnCount(2)
            dialog.paTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(exeldf)):
                for j in range(2):
                    item = QTableWidgetItem(str(exeldf.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.paTable.setItem(i, j, item)
            dialog.paTable.resizeColumnsToContents()
            dialog.paTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.num = 1
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # def reverse_sunggong_chart(self):
# ====================성공률 top10=============================================================
    def calculate_success_rates(self, df):
        # '심사승인'인 데이터만 필터링
        df2 = df.copy()
        df2.loc[:, '주선인'] = df2['주선인'].str.split(',')
        df2 = df2.iloc[:, 2:4]
        exploded_df2 = df2.explode('주선인')
        exploded_df2 = exploded_df2.reset_index(drop=True)
        success_df = df2[df2['성공여부'] == '심사승인']
        jusunin_df = success_df.loc[:, '주선인':'성공여부']
        exploded_df = jusunin_df.explode('주선인')
        exploded_df = exploded_df.reset_index(drop=True)
        # 주선인별 데이터 수 계산
        counts = exploded_df2['주선인'].value_counts()
        # 데이터 수가 50개 이상인 주선인만 선택
        qualified_counts = counts[counts >= 50]
        # 성공률 계산
        success_counts = exploded_df['주선인'].value_counts()
        success_counts = success_counts[success_counts >= 40]
        success_rates = (success_counts / qualified_counts) * 100
        # 성공률 상위 10개 추출
        top_10_success_rates = success_rates.nlargest(10)
        return top_10_success_rates


    def create_top_success_rates_bar_chart(self, dialog, df):
        df2 = df.copy()
        df2.loc[:, '주선인'] = df2['주선인'].str.split(',')
        df2 = df2.iloc[:, 2:4]
        success_df = df2[df2['성공여부'] == '심사승인']
        jusunin_df = success_df.loc[:, '주선인':'성공여부']
        # jusunin_df.loc[:, '주선인'] = success_df['주선인'].str.split(',')
        exploded_df = jusunin_df.explode('주선인')
        exploded_df = exploded_df.reset_index(drop=True)
        # 성공률 계산
        success_counts = exploded_df['주선인'].value_counts()
        success_counts = success_counts[success_counts >= 40]
        new_order = [
            '삼성증권㈜',
            '한국투자증권㈜',
            '유안타증권㈜',
            '엔에이치투자증권주식회사',
            '하나증권주식회사',
            '신한투자증권 주식회사',
            'KB증권㈜',
            'IBK투자증권㈜',
            '키움증권㈜',
            '미래에셋증권 주식회사'
        ]
        reordered_success_counts = success_counts.reindex(new_order)
        top_10 = reordered_success_counts.head(10)
        self.df3 = top_10
        # 함수 호출
        top_10_success_rates = self.calculate_success_rates(df)
        # print(top_10_success_rates)
        # 그래프 생성
        fig = go.Figure(data=[go.Bar(x=top_10_success_rates.index, y=top_10_success_rates.values,
                                     text=top_10_success_rates.round(2).astype(str) + '%' + '\n'+ top_10.astype(str) + '건',
                                     textposition='auto')])  # 'auto'는 최적 위치에 자동 배치
        fig.update_layout(title='성공률 주선인 Top10(상장승인 50건 이상)')

        # HTML 파일로 저장
        fig.write_html("성공률 top10.html")
        html_path = os.path.abspath("성공률 top10.html")
        dialog.gamsain_webEngineView.setUrl(QUrl.fromLocalFile(html_path))

        exeldf = self.df3.to_frame(name='성공횟수')
        exeldf.reset_index(inplace=True)
        exeldf.rename(columns={'index': '회사', '성공횟수': '건수'}, inplace=True)
        self.df4 = exeldf
        tableHeader = ['주선인', '건수']
        # print(len(df))
        dialog.paTable.setRowCount(len(exeldf))
        dialog.paTable.setColumnCount(2)
        dialog.paTable.setHorizontalHeaderLabels(tableHeader)
        for i in range(len(exeldf)):
            for j in range(2):
                item = QTableWidgetItem(str(exeldf.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                dialog.paTable.setItem(i, j, item)
        dialog.paTable.resizeColumnsToContents()
        dialog.paTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.num = 2
#================승인횟수 Top10==========================================================================

    def create_gamsain_barchart(self, dialog, column_series, threshold=0.01):
        try:
            processed_column = self.process_column(column_series)  # 주선인 열 처리
            value_counts = processed_column.value_counts()
            total_count = value_counts.sum()
            filtered_counts = value_counts[value_counts / total_count >= threshold]
            etc_count = value_counts[value_counts / total_count < threshold].sum()
            filtered_counts['etc'] = etc_count

            # top 10 추출
            top_10_counts = filtered_counts.nlargest(10)
            self.df3 = top_10_counts
            # 그래프 생성
            fig = go.Figure(data=[go.Bar(x=top_10_counts.index, y=top_10_counts.values,
                                         text=top_10_counts.round(2).astype(str) + '건',
                                         textposition='auto')])
            fig.update_layout(title='상장 주선인 Top10(상장승인 50건 이상)')

            # HTML 파일로 저장
            fig.write_html("상장 주선인 Top10.html")
            html_path = os.path.abspath("상장 주선인 Top10.html")
            dialog.gamsain_webEngineView.setUrl(QUrl.fromLocalFile(html_path))

            exeldf = self.df3.to_frame(name='성공횟수')
            exeldf.reset_index(inplace=True)
            exeldf.rename(columns={'index': '회사', '성공횟수': '건수'}, inplace=True)
            self.df4 = exeldf
            tableHeader = ['주선인', '건수']
            # print(len(df))
            dialog.paTable.setRowCount(len(exeldf))
            dialog.paTable.setColumnCount(2)
            dialog.paTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(exeldf)):
                for j in range(2):
                    item = QTableWidgetItem(str(exeldf.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.paTable.setItem(i, j, item)
            dialog.paTable.resizeColumnsToContents()
            dialog.paTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.num = 3

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def toExel(self):
        df = self.df4
        if self.num == 1:
            df.to_excel("IPO 상장주선인(파트너사) 승인 전체 데이터.xlsx", index=True)
        elif self.num == 2:
            df.to_excel("IPO 상장주선인(파트너사) 승인 횟수 Top10 데이터.xlsx", index=True)
        elif self.num == 3:
            df.to_excel("IPO 상장주선인(파트너사) 승인 성공률 Top10 데이터.xlsx", index=True)