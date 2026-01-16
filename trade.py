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


# 1. 화면 설정 (Wide Mode) - 무조건 맨 위에 있어야 함
st.set_page_config(page_title="농수산식품 수출 분석", layout="wide")

# ---------------------------------------------------------
# CSS: 다크모드, 폰트 크기, 여백 최적화
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    /* 환율 숫자 스타일 */
    [data-testid="stMetricValue"] {
        font-size: 24px; 
        font-weight: bold;
        color: #FFFFFF !important;
    }
    [data-testid="stMetricLabel"] {
        color: #CCCCCC !important;
        font-size: 14px;
    }
    /* 상단 여백 설정 */
    .block-container {
        padding-top: 3.5rem; 
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 차트 스타일 설정
plt.style.use('dark_background')

# 한글 폰트 설정
if os.name == 'nt': 
    plt.rc('font', family='Malgun Gothic') 
    plt.rc('axes', unicode_minus=False)

# ---------------------------------------------------------
# 2. 상단 헤더 & 환율 정보
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([1, 2])
with col_head1:
    st.title("📊 농수산식품 수출")
    st.caption(f"제작일: {datetime.now().strftime('%Y-%m-%d')}")

with col_head2:
    # 환율 정보
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🇺🇸 USD", "1,425.5", "▲2.5")
    c2.metric("🇯🇵 JPY", "955.2", "▼1.3")
    c3.metric("🇪🇺 EUR", "1,540.1", "▲5.0")
    c4.metric("🇨🇳 CNY", "198.5", "-0.0")

st.write("---")

# ---------------------------------------------------------
# 3. 데이터 로드 및 전처리 (try 시작)
# ---------------------------------------------------------
file_name = "한국농수산식품유통공사_국가별 연도별 수출실적_20241231.csv"

try:
    # 데이터 읽기
    try:
        df_raw = pd.read_csv(file_name)
    except UnicodeDecodeError:
        df_raw = pd.read_csv(file_name, encoding='cp949')

    # 전처리
    def clean_country_name(name):
        return name.replace(' - ', '').replace(' ', '')

    df_raw['clean_name'] = df_raw['구분'].apply(clean_country_name)
    df_clean = df_raw[df_raw['clean_name'] != '총합'].copy()

    # 좌표 데이터
    country_coords = {
        '일본': [36.20, 138.25], '중국': [35.86, 104.19], '홍콩': [22.31, 114.16],
        '대만': [23.69, 120.96], '미국': [37.09, -95.71], '캐나다': [56.13, -106.34],
        '베트남': [14.05, 108.27], '태국': [15.87, 100.99], '인도네시아': [-0.78, 113.92],
        '필리핀': [12.87, 121.77], '말레이시아': [4.21, 101.97], '네덜란드': [52.13, 5.29],
        '영국': [55.37, -3.43], '독일': [51.16, 10.45], '프랑스': [46.22, 2.21],
        '러시아': [61.52, 105.31], '몽골': [46.86, 103.84], '카자흐스탄': [48.01, 66.92],
        '멕시코': [23.63, -102.55], '브라질': [-14.23, -51.92], '호주': [-25.27, 133.77],
        '뉴질랜드': [-40.90, 174.88], 'UAE': [23.42, 53.84], '사우디아라비아': [23.88, 45.07]
    }

    map_data = []
    for index, row in df_raw.iterrows():
        name = row['clean_name']
        if name in country_coords:
            lat, lon = country_coords[name]
            value = row['24년수출금액']
            map_data.append({
                '국가명': name, 'lat': lat, 'lon': lon, '수출액': value,
                '수출액_표시': f"{value:,.0f}"
            })
    df_map = pd.DataFrame(map_data)

    # ---------------------------------------------------------
    # 4. 탭 구성
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["📊 종합 분석 (차트 & 다운로드)", "🌍 3D 지도로 보기"])

    # === [탭 1] 종합 분석 ===
    with tab1:
        col_left, col_right = st.columns([2, 1]) 
        
        # [왼쪽] 막대 그래프
        with col_left:
            st.markdown("##### 🏆 수출 상위 20개국")
            df_top20 = df_clean.sort_values(by='24년수출금액', ascending=False).head(20)
            
            fig, ax = plt.subplots(figsize=(10, 5)) 
            sns.barplot(data=df_top20, x='clean_name', y='24년수출금액', palette='rocket', ax=ax)
            
            ax.set_ylabel("수출금액", color='gray')
            ax.set_xlabel("", color='white') 
            ax.tick_params(axis='x', rotation=45, colors='white') 
            ax.tick_params(axis='y', colors='gray')
            ax.grid(axis='y', linestyle='--', alpha=0.3) 
            sns.despine(left=True, bottom=True)
            st.pyplot(fig)

        # [오른쪽] 원형 그래프 + CSV 다운로드
        with col_right:
            st.markdown("##### 🥧 상위 5개국 비중")
            
            df_sorted = df_clean.sort_values(by='24년수출금액', ascending=False)
            top5 = df_sorted.head(5)
            others_sum = df_sorted.iloc[5:]['24년수출금액'].sum()
            
            pie_labels = top5['clean_name'].tolist() + ['기타']
            pie_values = top5['24년수출금액'].tolist() + [others_sum]
            explode = [0.05] * len(pie_labels) 
            
            fig2, ax2 = plt.subplots(figsize=(4, 4))
            
            wedges, texts, autotexts = ax2.pie(
                pie_values, labels=pie_labels, autopct='%1.0f%%', 
                startangle=90, colors=sns.color_palette('Set3'),
                explode=explode, shadow=True,
                wedgeprops={'width': 0.5, 'edgecolor': 'black'}
            )
            for text in texts: text.set_color('white'); text.set_fontsize(9)
            for autotext in autotexts: autotext.set_color('black'); autotext.set_weight('bold')
            
            st.pyplot(fig2)
            
            st.write("") 
            st.markdown("##### 💾 데이터 다운로드")
            csv = df_clean.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📄 전체 데이터 CSV 받기",
                data=csv,
                file_name='2024_수출실적_전체.csv',
                mime='text/csv',
                use_container_width=True
            )

    # === [탭 2] 3D 지도 ===
    with tab2:
        layer = pdk.Layer(
            "ColumnLayer",
            data=df_map,
            get_position='[lon, lat]',
            get_elevation='수출액',
            elevation_scale=0.05,
            radius=200000,
            get_fill_color='[0, 255, 255, 200]', 
            pickable=True, extruded=True
        )
        view_state = pdk.ViewState(longitude=126.97, latitude=37.56, zoom=1.5, pitch=45)
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{국가명}\n수출액: {수출액_표시}"},
            map_style=pdk.map_styles.CARTO_DARK
        )
        st.pydeck_chart(r)

    # ---------------------------------------------------------
    # 5. 마무리 (3단 따봉 - 줄바꿈 & 가운데 정렬 완벽 수정)
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

except FileNotFoundError:
    st.error(f"❌ '{file_name}' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 에러 발생: {e}")