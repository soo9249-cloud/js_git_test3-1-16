#app.py > 배포할 파일
# Flask >배포가 어렵다 / streamlit > 배포가 쉽다. 조금 더 제한적이다.

import streamlit as st
import pandas as pd # 그래프 그려주는 놈(그림, 차트)
import numpy as np # 다차원 연산시켜주는 놈(엑셀 활용)
import matplotlib.pyplot as plt # 시각화 도구(차트, 그래프) -> 더 이쁘게 그려준다
import seaborn as sns 
import os
if os.name == 'nt':  # 윈도우 사용자라면
    plt.rc('font', family='Malgun Gothic') 
    plt.rc('axes', unicode_minus=False)
# pip install (이름) (이름) > 터미널에 한번에 입력하면 한번에 설치 가능

st.title("📊 국세청 근로소득 데이터 분석기")

# 데이터 불러오기

file_path="국세청_근로소득 백분위(천분위) 자료_20241231.csv" # 데이터 경로  ./어디/어디/파일명 > 현재위치에서 데이터라는 폴더로 가서 파일을 찾아오라는 뜻이다. 
# ../ > 상위폴더로 이동 (현재보다 위에 있으면 문을 열고 나가야됨) 

try : 
    
    # 자료 읽기 
    df = pd.read_csv(file_path,encoding='euc-kr') #df=dataframe
    st.success("데이터를 성공적으로 불러 왔습니다! ✅")

    # 데이터 미리 보기
    st.subheader("📝 데이터 확인하기")
    st.dataframe(df.head()) #표 상단 5줄 보여주기 (() 생략하면 5개, 10개 보고싶으면 10을 head()안에 쓰면 된다.)

    # 데이터 분석 그래프
    st.subheader("📉 항목별 분포 그래프")

    # 분석하고 싶은 열 이름을 선택
    # 예를 들어 급여나 인원 같은 숫자 데이터가 있는 칸을 골라야 한다. 
    column_names=df.columns.tolist() # 해당 열의 이름, 제목을 갖고 온다는 뜻(?)
    selected_col=st.selectbox("분석할 항목을 선택하세요: ", column_names)

    # 그래프 그리기(seaborn 사용)
    fig, ax=plt.subplots(figsize=(10,5))   # fig는 figure의 약자 , fig는 그래프의 전체 사이즈고 ax는 그래프가 그려지는 공간
    sns.histplot(df[selected_col], ax=ax, color="#99CCFF",kde=True) 
    # seaborn의 histplot을 사용해서 히스토그램 그리기 RGB #RRCCFF(2자리씩 RGB) + 04?뭐 이런거 붙으면 투명도 # 그라데이션 넣기도 가능
    plt.title(f"[{selected_col}] 분포 확인") # 그래프 맨 위에 제목 넣기
    plt.xlabel(selected_col) # x축 제목(가로축) 예: (   급여액)
    plt.ylabel("빈도수") # y축 제목(세로축) 얼마나 자주 나오는지... 

    # streamlit 웹 화면에 그래프 표시
    st.pyplot(fig)

# 여기까지 기본사항(오류가 없을 때 이렇게 처리하라는 뜻)

# 오류가 생겼을 때


except FileNotFoundError:  # 파일명이 잘못되었을 때
    st.error(f" ❌ '{file_path}' 파일을 찾을 수 없습니다. 파일명이 정확한지 확인해 주세요")
except Exception as e: # syntheic 에러>무슨 에러?
    st.error(f" ❌ 에러가 발생했습니다.{e}")
# e는 파이썬에서 갖고 있는 모든 syntax error를 다 포함하는 기본 변수이다.

