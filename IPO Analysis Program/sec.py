import traceback

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn.objects as so
# 한글 폰트 문제 해결
# matplotlib은 한글 폰트를 지원하지 않음
# os정보
import platform

from PyQt5.QtWidgets import QTableWidgetItem
# font_manager : 폰트 관리 모듈
# rc : 폰트 변경 모듈
from matplotlib import font_manager, rc

# unicode 설정
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')  # os가 macos
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'  # os가 windows
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("Unknown System")

def getdata():
    df = pd.read_csv('./IPO현황_최종.csv', encoding='cp949')

    # 아래의 컬럼들을 ETC로 통합
    df['대분류'] = df['대분류'].replace({'도매 및 소매업': 'etc', '부동산업': 'etc', '건 설 업': 'etc', '운수 및 창고업': 'etc',
                                   '사업시설 관리, 사업 지원 및 임대 서비스업': 'etc', '전기, 가스, 증기 및 공기 조절 공급업': 'etc',
                                   '교육서비스업': 'etc', '예술, 스포츠 및 여가관련 서비스업': 'etc',
                                   '농업, 임업 및 어업': 'etc', '수도, 하수 및 폐기물 처리, 원료 재생업': 'etc',
                                   '숙박 및 음식점업': 'etc', '협회 및 단체, 수리 및 기타 개인 서비스업': 'etc', '광업': 'etc'
                                   })

    # 컬럼명을 수정하여 차트의 범례 부분을 수정
    df['대분류'] = df['대분류'].replace('전문, 과학 및 기술 서비스업', '전문과학기술서비스업')

    # 성공여부 컬럼에서 심사철회 -> 심사 미승인으로 변경
    df['성공여부'] = df['성공여부'].replace(['심사철회'], '심사미승인')

    # 데이터프레임 컬럼에 성공여부가 있는지 확인
    if '성공여부' in df.columns:
        success_df = df[df['성공여부'] == '심사승인']  # 성공여부가 "심사승인" 행들을 가지고온다.
        fail_df = df[df['성공여부'] == '심사미승인']  # 성공여부가 "심사미승인" 행들을 가지고 온다.
        ing_df = df[df['성공여부'] == '심사중']  # 성공여부가 "심사중" 행들을 가지고온다.
    else:
        #성공여부 컬럼이 없는 경우 빈 데이터프레임을 할당
        success_df = pd.DataFrame()
        ing_df = pd.DataFrame()
        fail_df = pd.DataFrame()
    # print(df['대분류'].value_counts())
    # print(success_df['대분류'].value_counts())
    return df, success_df, ing_df, fail_df

def create_chart(df, success_df, ing_df, fail_df, num):
    order = ['제조업1', '제조업2', '제조업3', '제조업4', '금융 및 보험업', '정보통신업', '전문과학기술서비스업', 'etc']
    fig = plt.figure(figsize=(10, 6))

    if num == 1:
        # 사용자 정렬
        try :
            # 전체 스택 차트 생성
            ax1 = fig.add_subplot(1,1,1)
            sns.countplot(df, x='대분류', hue='성공여부', order=order, ax=ax1, palette='Set1')
            plt.title("전체 업종")
            plt.tight_layout()
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        # 데이터 sortcount
        success_counts = success_df['대분류'].value_counts()
        # print(success_counts)
        ing_counts = ing_df['대분류'].value_counts()
        # print(ing_counts)
        fail_counts = fail_df['대분류'].value_counts()
        print(fail_counts)

        # 왼쪽 그래프
        for i, count in enumerate(success_counts):
            if i == 0:
                a = 4
                leftBar(a, count)
            elif i == 1:
                a = 3
                leftBar(a, count)
            elif i == 2:
                a = 2
                leftBar(a, count)
            elif i == 3:
                a = 5
                leftBar(a, count)
            elif i == 4:
                a = 1
                leftBar(a, count)
            elif i == 5:
                a = 0
                leftBar(a, count)
            elif i == 6:
                a = 7
                leftBar(a, count)
            elif i == 7:
                a = 6
                leftBar(a, count)

        # 가운데 그래프
        for i, count in enumerate(ing_counts):
            if i == 0:
                a = 5
                centerBar(a, count)
            elif i == 1:
                a = 3
                centerBar(a, count)
            elif i == 2:
                a = 2
                centerBar(a, count)
            elif i == 3:
                a = 0
                centerBar(a, count)
            elif i == 4:
                a = 1
                centerBar(a, count)
            elif i == 5:
                a = 4
                centerBar(a, count)
            elif i == 6:
                a = 6
                centerBar(a, count)
            elif i == 7:
                a = 7
                centerBar(a, count)
        # 오른쪽 그래프
        for i, count in enumerate(fail_counts):
            if i == 0:
                a = 2
                rightBar(a, count)
            elif i == 1:
                a = 1
                rightBar(a, count)
            elif i == 2:
                a = 5
                rightBar(a, count)
            elif i == 3:
                a = 3
                rightBar(a, count)
            elif i == 4:
                a = 0
                rightBar(a, count)
            elif i == 5:
                a = 6
                rightBar(a, count)
            elif i == 6:
                a = 7
                rightBar(a, count)
            elif i == 7:
                a = 4
                rightBar(a, count)

        plt.savefig('전체.png', bbox_inches='tight')  # 그래프를 이미지 파일로 저장

    elif num == 2:
        # 심사 중 차트 생성
        plt.clf()
        ax3 = fig.add_subplot(1, 1, 1)
        sns.countplot(x='대분류', hue='성공여부', data=ing_df, order=order, dodge=False, ax=ax3, palette='Set1')
        plt.title("현재 심사 중인 현황")
        plt.tight_layout()
        plt.savefig('심사중.png', bbox_inches='tight')

    elif num == 3:
        # 심사 실패 차트 생성
        plt.clf()
        ax4 = fig.add_subplot(1, 1, 1)
        sns.countplot(x='대분류', hue='성공여부', data=fail_df, order=order, dodge=False, ax=ax4, palette='Set1')
        plt.title("업종별 심사실패 현황")
        plt.tight_layout()
        plt.savefig('심사실패.png', bbox_inches='tight')

    elif num == 4:
        # 심사 승인 차트 생성
        plt.clf()  # 차트 초기화
        ax2 = fig.add_subplot(1, 1, 1)
        sns.countplot(x='대분류', hue='성공여부', data=success_df, order=order, dodge=False, ax=ax2, palette='Set1')

        plt.title("업종별 심사승인 현황")
        plt.tight_layout()
        plt.savefig('심사성공.png', bbox_inches='tight')
        plt.close()

def leftBar(a, count):
    plt.text(a, count, str(count), ha='right', va='bottom')

def centerBar(a, count):
    plt.text(a, count, str(count), ha='right', va='bottom')

def rightBar(a, count):
    plt.text(a, count, str(count), ha='left', va='bottom')
class main:
    df, success_df, ing_df, fail_df = getdata()

    total_df_file = df['대분류'].value_counts().reset_index()
    total_df_file.columns = ['업종', '법인 수']

    success_df_file = success_df['대분류'].value_counts().reset_index()
    success_df_file.columns = ['업종', '법인 수']

    ing_df_file = ing_df['대분류'].value_counts().reset_index()
    ing_df_file.columns = ['업종', '법인 수']

    fail_df_file = fail_df['대분류'].value_counts().reset_index()
    fail_df_file.columns = ['업종', '법인 수']

    def summary(self, dialog,  df):
        try:
            tableHeader = ['업종', '법인 수']
            dialog.secTable.setRowCount(len(df))
            dialog.secTable.setColumnCount(2)
            dialog.secTable.setHorizontalHeaderLabels(tableHeader)
            for i in range(len(df)):
                for j in range(2):
                    item = QTableWidgetItem(str(df.iloc[i, j]))  # 문자열로 변환하여 QTableWidgetItem 생성
                    dialog.secTable.setItem(i, j, item)
            dialog.secTable.resizeColumnsToContents()   # 컬럼 사이즈를 글씨크기에 맞게 조정
        except Exception as e:
            print(e)
            print(traceback.format_exc())


