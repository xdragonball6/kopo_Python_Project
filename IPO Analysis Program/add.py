import os
import traceback

import pandas as pd
import folium
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class add:
    # -- main file read
    df = pd.read_csv('./IPO현황_최종.csv', encoding='cp949')

    # -- 승인별 df
    readyDf = df[df['성공여부'].str.contains('심사중')]
    failDf = df[df['성공여부'].str.contains('심사철회|심사미승인')]
    okDf = df[df['성공여부'].str.contains('심사승인')]

    allCount = 0

    def btn(self, dialog):
        dialog.addAllBtn.clicked.connect(lambda: self.graphAll(dialog))
        dialog.addReadyBtn.clicked.connect(lambda: self.graphReady(dialog))
        dialog.addFailBtn.clicked.connect(lambda: self.graphFail(dialog))
        dialog.addOkBtn.clicked.connect(lambda: self.graphOk(dialog))

    def countDf(self, df):
        df2 = df['주소'].str[:2]
        seoulCount = len(df[df2.str.contains('서울')])
        sudogwonCount = len(df[df2.str.contains('인천|경기')])
        gangwonCount = len(df[df2.str.contains('강원')])
        daejeonAndCount = len(df[df2.str.contains('대전|세종|충청|충남|충북|천안')])
        gwangjuAndCount = len(df[df2.str.contains('광주|전라|전남|전북')])
        busanAndCount = len(df[df2.str.contains('부산|울산|대구|경상|경남|경북')])
        jejuCount = len(df[df2.str.contains('제주')])
        col_names = ['지역', 'count', 'lat', 'lot']
        # 데이터프레임 생성
        result_df = pd.DataFrame({
            '지역': ['서울', '인천|경기', '강원', '대전|세종|충청|충남|충북|천안', '광주|전라|전남|전북', '부산|울산|대구|경상|경남|경북', '제주'],
            'count': [seoulCount, sudogwonCount, gangwonCount, daejeonAndCount, gwangjuAndCount, busanAndCount, jejuCount],
            '위도': [37.5665, 37.4563, 37.8861, 36.3504, 35.1595, 35.1796, 33.4996],
            '경도': [126.9780, 126.7052, 127.7298, 127.3845, 126.8526, 129.0756, 126.5312]
        })
        # print(result_df)
        return result_df


    def graphAll(self, dialog):
        seoul_map = folium.Map(
            location=[35.55, 126.38],
            zoom_start=7,
            tiles='CartoDB positron'
        )

        df = self.countDf(self.df)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            if ban[0] / 10 > 10:
                banNum = int(ban[0] / 10)
            elif ban[0] < 10:
                banNum = 1

            if banNum >= 50:
                result = 30
            elif banNum >= 40:
                result = 25
            elif banNum >= 30:
                result = 20
            elif banNum >= 20:
                result = 15
            elif banNum >= 10:
                result = 10
            else:
                result = ban[0]

            # print(result)

            folium.CircleMarker(
                [lat, lng],
                radius=result,  # 원의 반지름
                color='navy',  # 원의 둘레 색상
                fill=True,  # 원 안을 채우기
                fill_color='navy',  # 원 안의 색상
                fill_opacity=0.7,  # 원의 투명도
            ).add_to(seoul_map)
            # print(df['count'][count])
            count += 1

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            test = f"{name}, {df['count'][count]}"
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(test, max_width=len(name)),
            ).add_to(seoul_map)
            count += 1

        seoul_map.save('map.html')
        # 현재 스크립트 파일의 디렉토리 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # map.html 파일 경로 생성
        html_file_path = os.path.join(current_dir, 'map.html')
        dialog.mapGraph.setUrl(QUrl.fromLocalFile(html_file_path))

        tableHeader = ['지역', '법인 수']
        # print(len(df))
        try:
            dialog.addTable.setRowCount(len(df))
            dialog.addTable.setColumnCount(2)
            dialog.addTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(df)):
                print('i', i)
                for j in range(2):
                    print('j', j)
                    item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.addTable.setItem(i, j, item)
                    print(df.iloc[i, j])

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def graphReady(self, dialog):
        seoul_map = folium.Map(
            location=[35.55, 126.38],
            zoom_start=7,
            tiles='CartoDB positron'
        )
        df = self.countDf(self.readyDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            # print(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=ban[0]+10,  # 원의 반지름
                color='green',  # 원의 둘레 색상
                fill=True,  # 원 안을 채우기
                fill_color='green',  # 원 안의 색상
                fill_opacity=0.7,  # 원의 투명도
            ).add_to(seoul_map)
            count += 1

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            test = f"{name}, {df['count'][count]}"
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(test, max_width=len(name)),
            ).add_to(seoul_map)
            count += 1

        seoul_map.save('mapReady.html')
        # 현재 스크립트 파일의 디렉토리 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # map.html 파일 경로 생성
        html_file_path = os.path.join(current_dir, 'mapReady.html')
        dialog.mapGraph.setUrl(QUrl.fromLocalFile(html_file_path))

        tableHeader = ['지역', '법인 수']
        # print(len(df))
        try:
            dialog.addTable.setRowCount(len(df))
            dialog.addTable.setColumnCount(2)
            dialog.addTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(df)):
                print('i', i)
                for j in range(2):
                    print('j', j)
                    item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.addTable.setItem(i, j, item)
                    print(df.iloc[i, j])

        except Exception as e:
            print(e)
            print(traceback.format_exc())




    def graphFail(self, dialog):
        seoul_map = folium.Map(
            location=[35.55, 126.38],
            zoom_start=7,
            tiles='CartoDB positron'
        )
        df = self.countDf(self.failDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            # print(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=ban[0]+10,  # 원의 반지름
                color='red',  # 원의 둘레 색상
                fill=True,  # 원 안을 채우기
                fill_color='red',  # 원 안의 색상
                fill_opacity=0.7,  # 원의 투명도
            ).add_to(seoul_map)
            count += 1

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            test = f"{name}, {df['count'][count]}"
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(test, max_width=len(name)),
            ).add_to(seoul_map)
            count += 1

        seoul_map.save('mapFail.html')
        # 현재 스크립트 파일의 디렉토리 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # map.html 파일 경로 생성
        html_file_path = os.path.join(current_dir, 'mapFail.html')
        dialog.mapGraph.setUrl(QUrl.fromLocalFile(html_file_path))

        tableHeader = ['지역', '법인 수']
        # print(len(df))
        try:
            dialog.addTable.setRowCount(len(df))
            dialog.addTable.setColumnCount(2)
            dialog.addTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(df)):
                print('i', i)
                for j in range(2):
                    print('j', j)
                    item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.addTable.setItem(i, j, item)
                    print(df.iloc[i, j])

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def graphOk(self, dialog):
        seoul_map = folium.Map(
            location=[35.55, 126.38],
            zoom_start=7,
            tiles='CartoDB positron'
        )
        df = self.countDf(self.okDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            # print(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=ban[0]+10,  # 원의 반지름
                color='blue',  # 원의 둘레 색상
                fill=True,  # 원 안을 채우기
                fill_color='blue',  # 원 안의 색상
                fill_opacity=0.7,  # 원의 투명도
            ).add_to(seoul_map)
            count += 1

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            test = f"{name}, {df['count'][count]}"
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(test, max_width=len(name)),
            ).add_to(seoul_map)
            count += 1

        seoul_map.save('mapOk.html')
        # 현재 스크립트 파일의 디렉토리 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # map.html 파일 경로 생성
        html_file_path = os.path.join(current_dir, 'mapOk.html')
        dialog.mapGraph.setUrl(QUrl.fromLocalFile(html_file_path))

        tableHeader = ['지역', '법인 수']
        # print(len(df))
        try:
            dialog.addTable.setRowCount(len(df))
            dialog.addTable.setColumnCount(2)
            dialog.addTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(df)):
                print('i', i)
                for j in range(2):
                    print('j', j)
                    item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.addTable.setItem(i, j, item)
                    print(df.iloc[i, j])

        except Exception as e:
            print(e)
            print(traceback.format_exc())









