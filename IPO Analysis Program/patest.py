import os, sys
import traceback

import pandas as pd
import plotly.graph_objects as go
from PyQt5.QtCore import QUrl

# Test 클래스 정의
class Gamsain:
    def process_column(self, column_series):
        if column_series.str.contains(',').any():
            processed_values = column_series.str.split(',')
            return processed_values.explode()
        else:
            return column_series

    def create_gamsain_chart(self, dialog, column_series, threshold=0.01):
        # print(column_series)
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

