import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import os
from mpl_toolkits.mplot3d import Axes3D # 3D 그래프용
import pydeck as pdk
import os
from datetime import datetime


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 화면 설정 (Wide Mode)
st.set_page_config(page_title="2024 직장인 연봉 분석", layout="wide")

# ---------------------------------------------------------
# 스타일링 (다크모드 + 폰트)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    /* 메트릭(숫자) 스타일 */
    [data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: bold;
        color: #00FFCC !important; /* 형광 민트색 */
    }
    [data-testid="stMetricLabel"] {
        color: #CCCCCC !important;
    }
    /* 입력창 스타일 */
    .stTextInput input {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

plt.style.use('dark_background')
if os.name == 'nt': 
    plt.rc('font', family='Malgun Gothic') 
    plt.rc('axes', unicode_minus=False)

# ---------------------------------------------------------
# 2. 데이터 로드 및 전처리
# ---------------------------------------------------------
file_name = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(file_name)
    except:
        df = pd.read_csv(file_name, encoding='cp949')
    
    # 숫자 변환
    def parse_percentile(x):
        return float(x.replace('상위', '').replace('%', '').replace(' ', ''))
    
    df['percentile'] = df['구분'].apply(parse_percentile)
    
    # 1인당 평균 급여/세금 계산
    df['avg_salary'] = df['총급여'] * 100000000 / df['인원']
    df['avg_tax'] = df['결정세액'] * 100000000 / df['인원']
    df['effective_tax_rate'] = (df['avg_tax'] / df['avg_salary']) * 100
    
    return df

try:
    df = load_data()
    
    # ---------------------------------------------------------
    # 3. 상단 헤더 & 핵심 요약
    # ---------------------------------------------------------
    st.title("💰 대한민국 직장인 연봉 분석기 💰")
    st.caption("자료 출처: 국세청 근로소득 백분위 통계")
    
    st.write("---")
    
    top_0_1 = df[df['percentile'] == 0.1]['avg_salary'].values[0]
    top_1 = df[df['percentile'] == 1.0]['avg_salary'].values[0]
    median = df[df['percentile'] == 50.0]['avg_salary'].values[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👑 상위 0.1% 평균 연봉", f"{top_0_1/100000000:.1f}억 {top_0_1%100000000/10000:,.0f}만원")
    with col2:
        st.metric("🥇 상위 1% 평균 연봉", f"{top_1/100000000:.1f}억 {top_1%100000000/10000:,.0f}만원")
    with col3:
        st.metric("😐 중위(50%) 평균 연봉", f"{median/10000:,.0f}만원")
        
    st.write("---")

    # ---------------------------------------------------------
    # 4. 탭 구성
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["📊 전체 소득 분포 분석", "📍 내 연봉 순위 찾기"])
    
    # === [탭 1] 전체 분석 차트 ===
    with tab1:
        # ★★★ 여기에 다운로드 버튼 추가! ★★★
        st.markdown("##### 💾 데이터 다운로드")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📄 분석 데이터 전체 받기 (CSV)",
            data=csv,
            file_name='2024_연봉분석_결과.csv',
            mime='text/csv'
        )
        st.write("") # 여백

        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("##### 📈 소득 분위별 평균 연봉")
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            sns.lineplot(data=df, x='percentile', y='avg_salary', color='#00FFCC', ax=ax1, linewidth=2)
            ax1.fill_between(df['percentile'], df['avg_salary'], color='#00FFCC', alpha=0.1)
            ax1.set_xlabel("소득 분위 (상위 %)", color='white')
            ax1.set_ylabel("평균 연봉 (원)", color='white')
            ax1.invert_xaxis()
            
            # Y축 단위 억/천만
            current_values = plt.gca().get_yticks()
            plt.gca().set_yticklabels(['{:,.0f}억'.format(x/100000000) for x in current_values])
            st.pyplot(fig1)
            
        with col_chart2:
            st.markdown("##### 💸 실효 세율 분포")
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.lineplot(data=df, x='percentile', y='effective_tax_rate', color='#FF5555', ax=ax2, linewidth=2)
            ax2.set_xlabel("소득 분위 (상위 %)", color='white')
            ax2.set_ylabel("실효 세율 (%)", color='white')
            ax2.set_xlim(0, 100)
            st.pyplot(fig2)

    # === [탭 2] 내 연봉 순위 계산기 ===
    with tab2:
        st.subheader("내 연봉은 대한민국 상위 몇 %일까?")
        col_input, col_result = st.columns([1, 2])
        
        with col_input:
            input_salary_man = st.number_input("연봉 입력 (단위: 만원)", 100, 1000000, 4000, 100)
            my_salary = input_salary_man * 10000
            
            if st.button("내 순위 확인하기 🔍", use_container_width=True):
                my_percentile = 100.0
                for index, row in df.iterrows():
                    if my_salary >= row['avg_salary']:
                        my_percentile = row['percentile']
                        break
                st.session_state['result_p'] = my_percentile
                st.session_state['result_s'] = my_salary

        with col_result:
            if 'result_p' in st.session_state:
                p = st.session_state['result_p']
                s = st.session_state['result_s']
                st.info(f"연봉 **{s/10000:,.0f}만원**은...")
                st.markdown(f"## 🏆 상위 **{p}%** 입니다!")
                
                fig, ax = plt.subplots(figsize=(10, 2))
                ax.barh([0], [100], color='#333333', height=0.5)
                ax.axvline(x=p, color='#00FFCC', linewidth=5)
                ax.set_xlim(0, 100)
                ax.set_yticks([])
                ax.set_xticklabels(['상위 0%', '20%', '40%', '60%', '80%', '100%'])
                ax.text(p, 0.3, f'▼ 나 ({p}%)', color='#00FFCC', fontweight='bold', ha='center', fontsize=12)
                
                for spine in ax.spines.values(): spine.set_visible(False)
                ax.patch.set_alpha(0)
                st.pyplot(fig)

    # ---------------------------------------------------------
    # 5. 마무리 (따봉 & 다운로드)
    # ---------------------------------------------------------
    st.write("---") 
    
    # 5등분 (양옆 여백)
    c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
    
    # 스타일 정의 (가운데 정렬 + 줄바꿈)
    final_text = """
    <div style='text-align: center; color: white; font-size: 14px;'>
        분석 완료!<br>
        수고하셨습니다 👍
    </div>
    """

    with c2: 
        st.image("smile.png", use_container_width=True) # caption 삭제
        st.markdown(final_text, unsafe_allow_html=True) # 글씨를 따로 추가

    with c3: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)

    with c4: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)


except Exception as e:
    st.error(f"❌ 데이터 파일을 읽는 중 오류가 발생했습니다: {e}")