import os, sys
import traceback

import pandas as pd
import plotly.graph_objects as go
import self
from PyQt5.QtCore import QUrl

# Test 클래스 정의
class Gamsain:
    def process_column(self, column_series):
        if column_series.str.contains(',').any():
            processed_values = column_series.str.split(',')
            return processed_values.explode()
        else:
            return column_series
#====================전체 조회=============================================================
    def create_gamsain_chart(self, dialog, column_series, threshold=0.01):
        try:
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
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # def reverse_sunggong_chart(self):
# ====================성공률 top10=============================================================
    def calculate_success_rates(self, df):
        # '심사승인'인 데이터만 필터링
        success_df = df[df['성공여부'] == '심사승인']

        # 쉼표가 없는 데이터만 필터링
        success_df = success_df[~success_df['주선인'].str.contains(',')]

        # 주선인별 데이터 수 계산
        counts = df['주선인'].value_counts()

        # 데이터 수가 50개 이상인 주선인만 선택
        qualified_counts = counts[counts >= 50]

        # 성공률 계산
        success_counts = success_df['주선인'].value_counts()
        success_rates = (success_counts / qualified_counts) * 100

        # 성공률 상위 10개 추출
        top_10_success_rates = success_rates.nlargest(10)

        return top_10_success_rates


    def create_top_success_rates_bar_chart(self, dialog, df):
        # 함수 호출
        top_10_success_rates = self.calculate_success_rates(df)

        # 그래프 생성
        fig = go.Figure(data=[go.Bar(x=top_10_success_rates.index, y=top_10_success_rates.values,
                                     text=top_10_success_rates.round(2).astype(str) + '%',
                                     textposition='auto')])  # 'auto'는 최적 위치에 자동 배치
        fig.update_layout(title='성공률 주선인 Top10(상장승인 50건 이상)')

        # HTML 파일로 저장
        fig.write_html("성공률 top10.html")
        html_path = os.path.abspath("성공률 top10.html")
        dialog.gamsain_webEngineView.setUrl(QUrl.fromLocalFile(html_path))
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

            # 그래프 생성
            fig = go.Figure(data=[go.Bar(x=top_10_counts.index, y=top_10_counts.values,
                                         text=top_10_counts.round(2).astype(str) + '건',
                                         textposition='auto')])
            fig.update_layout(title='상장 주선인 Top10(상장승인 50건 이상)')

            # HTML 파일로 저장
            fig.write_html("상장 주선인 Top10.html")
            html_path = os.path.abspath("상장 주선인 Top10.html")
            dialog.gamsain_webEngineView.setUrl(QUrl.fromLocalFile(html_path))
        except Exception as e:
            print(e)
            print(traceback.format_exc())