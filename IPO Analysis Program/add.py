import os
import traceback

import pandas as pd
import folium
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class add:
    # -- main file read
    df = pd.read_csv('./IPO현황_최종.csv', encoding='cp949')

    # -- 승인별 df
    readyDf = df[df['성공여부'].str.contains('심사중')]
    failDf = df[df['성공여부'].str.contains('심사철회|심사미승인')]
    okDf = df[df['성공여부'].str.contains('심사승인')]

    downCount = 5   # 각 버튼이 클릭되는 것을 알리는 플래그 변수
    
    # 버튼 구현
    def btn(self, dialog):
        dialog.addAllBtn.clicked.connect(lambda: self.graphAll(dialog))
        dialog.addReadyBtn.clicked.connect(lambda: self.graphReady(dialog))
        dialog.addFailBtn.clicked.connect(lambda: self.graphFail(dialog))
        dialog.addOkBtn.clicked.connect(lambda: self.graphOk(dialog))
        dialog.addDown.clicked.connect(self.down)
        dialog.addTable.setEditTriggers(QAbstractItemView.NoEditTriggers) # QTable위젯 수정물가 코드
    
    # 각 함수에서 사용할 데이터 정제
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
            # '지역': ['서울', '인천|경기', '강원', '대전|세종|충청|충남|충북|천안', '광주|전라|전남|전북', '부산|울산|대구|경상|경남|경북', '제주'],
            '지역': ['서울특별시', '인천광역시, 경기도', '강원도', '대전광역시, 세종특별시, 충청남/북도', '광주광역시, 전라남/북도',
                    '부산산광역시, 울산광역시, 대구광역시, 경상남/북도', '제주특별자치시'],
            'count': [seoulCount, sudogwonCount, gangwonCount, daejeonAndCount, gwangjuAndCount, busanAndCount, jejuCount],
            '위도': [37.5665, 37.4563, 37.8861, 36.3504, 35.1595, 35.1796, 33.4996],
            '경도': [126.9780, 126.7052, 127.7298, 127.3845, 126.8526, 129.0756, 126.5312]
        })
        return result_df

    # 전체 버튼 클릭시 구현될 함수
    def graphAll(self, dialog):
        self.downCount = 0
        seoul_map = self.mapPrint()
        df = self.countDf(self.df)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            result = self.onePrint(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=result,  # 원의 반지름
                color='navy',  # 원의 둘레 색상
                fill=True,  # 원 안을 채우기
                fill_color='navy',  # 원 안의 색상
                fill_opacity=0.7,  # 원의 투명도
            ).add_to(seoul_map)
            count += 1

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            test = f"{name}, {df['count'][count]}"
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(test, max_width=len(name)),
                style='font-size: 20px'
            ).add_to(seoul_map)
            count += 1

        seoul_map.save('map.html')
        # 현재 스크립트 파일의 디렉토리 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # map.html 파일 경로 생성
        html_file_path = os.path.join(current_dir, 'map.html')
        dialog.mapGraph.setUrl(QUrl.fromLocalFile(html_file_path))

        self.summary(dialog, df)

    # 심사대기 버튼 클릭시 구현될 함수
    def graphReady(self, dialog):
        self.downCount = 1
        seoul_map = self.mapPrint()
        df = self.countDf(self.readyDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            result = self.onePrint(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=result,  # 원의 반지름
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

        self.summary(dialog, df)
    
    # 심사탈락 버튼 클릭시 구현될 함수
    def graphFail(self, dialog):
        self.downCount = 2
        seoul_map = self.mapPrint()
        df = self.countDf(self.failDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            result = self.onePrint(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=result,  # 원의 반지름
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

        self.summary(dialog, df)
    
    # 심사통과 버튼 클릭시 구현될 함수
    def graphOk(self, dialog):
        self.downCount = 3
        seoul_map = self.mapPrint()
        df = self.countDf(self.okDf)

        count = 0
        for name, lat, lng in zip(df.지역, df.위도, df.경도):
            ban = int(df['count'][count]),  # 원의 반지름
            result = self.onePrint(ban[0])

            folium.CircleMarker(
                [lat, lng],
                radius=result,  # 원의 반지름
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

        self.summary(dialog, df)

    def down(self):
        try:
            if self.downCount == 0:
                df = self.countDf(self.df)
                selected_columns = df.iloc[:, :2]  # 0번과 1번 열 선택
                selected_columns.to_excel("IPO 신청 전체 기업 수 데이터_주소별.xlsx", index=True)

            elif self.downCount == 1:
                df = self.countDf(self.readyDf)
                selected_columns = df.iloc[:, :2]  # 0번과 1번 열 선택
                selected_columns.to_excel("IPO 승인 대기 기업 수 데이터_주소별.xlsx", index=True)

            elif self.downCount == 2:
                df = self.countDf(self.failDf)
                selected_columns = df.iloc[:, :2]  # 0번과 1번 열 선택
                selected_columns.to_excel("IPO 실패 기업 수 데이터_주소별.xlsx", index=True)

            elif self.downCount == 3:
                df = self.countDf(self.okDf)
                selected_columns = df.iloc[:, :2]  # 0번과 1번 열 선택
                selected_columns.to_excel("IPO 승인 완료 기업 수 데이터_주소별.xlsx", index=True)

        except Exception as e:
            print(e)
            print(traceback.print_exc())

    # 지도에 원그래프 절대값 설정 
    def onePrint(self, ban):
        try:
            if self.downCount == 0:
                if ban >= 800:
                    result = 120
                elif ban >= 400:
                    result = 100
                elif ban >= 170:
                    result = 80
                elif ban >= 160:
                    result = 75
                elif ban >= 30:
                    result = 20
                elif ban >= 10:
                    result = 10
                else:
                    result = 3

                return result

            elif self.downCount == 1:
                if ban >= 20:
                    result = 20
                elif ban >= 10:
                    result = 10
                elif ban == 0:
                    result = 1
                else:
                    result = ban

                return result

            elif self.downCount == 2:
                if ban >= 100:
                    result = 60
                elif ban >= 60:
                    result = 35
                elif ban >= 30:
                    result = 20
                elif ban >= 25:
                    result = 15
                else:
                    result = 3

                return result

            elif self.downCount == 3:
                if ban >= 600:
                    result = 110
                elif ban >= 300:
                    result = 90
                elif ban >= 100:
                    result = 60
                elif ban >= 20:
                    result = 15
                elif ban >= 10:
                    result = 10
                else:
                    result = 3

                return result
        except Exception as e:
            print(e)
            print(traceback.print_exc())
    
    # 서머리 출력 함수
    def summary(self, dialog,  df):
        tableHeader = ['지역', '법인 수']

        dialog.addTable.setRowCount(len(df))
        dialog.addTable.setColumnCount(2)
        dialog.addTable.setHorizontalHeaderLabels(tableHeader)
        for i in range(len(df)):
            for j in range(2):
                item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                dialog.addTable.setItem(i, j, item)
        dialog.addTable.resizeColumnsToContents()   # 컬럼 사이즈를 글씨크기에 맞게 조정

    # 지도 생성 메서드
    def mapPrint(self):
        seoul_map = folium.Map(
            location=[35.55, 126.38],
            zoom_start=7,
            tiles='CartoDB positron'
        )
        return seoul_map









