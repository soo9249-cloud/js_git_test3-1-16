import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import random

# 1. 화면 설정
st.set_page_config(page_title="심심할 때 해보기", layout="wide")

# ---------------------------------------------------------
# [CSS] 디자인 (글씨 색상 강제 흰색 + 버튼 + 애니메이션)
# ---------------------------------------------------------
ufo_css = ""
for i in range(1, 11):
    left_pos = random.randint(5, 95)
    delay = random.uniform(0, 5)
    duration = random.uniform(5, 10)
    
    ufo_css += f"""
    .ufo-{i} {{
        position: fixed;
        left: {left_pos}%;
        top: -10%;
        font-size: {random.randint(30, 60)}px;
        z-index: 999;
        animation: drop {duration}s linear {delay}s forwards;
        opacity: 0.8;
        pointer-events: none;
    }}
    """

st.markdown(f"""
    <style>
    /* 1. 전체 배경 다크모드 & 글씨 흰색 강제 적용 */
    .stApp {{
        background-color: #0E1117;
        color: white !important;
    }}
    
    /* 2. 모든 제목(h1~h3), 본문(p), 라벨(label) 흰색 처리 */
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        color: white !important;
    }}
    
    /* 3. 버튼 스타일 (평소엔 어둡게, 마우스 올리면 밝게) */
    div.stButton > button {{
        width: 100%;
        background-color: #262730; 
        color: white !important; /* 버튼 글씨도 흰색 */
        border: 1px solid #4B4B4B;
        border-radius: 10px;
        padding: 15px;
        font-size: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background-color: #383a47; 
        color: #00FFCC !important; /* 마우스 올리면 형광색 */
        border: 1px solid #00FFCC;
    }}
    div.stButton > button p {{
        color: inherit !important; /* 버튼 안의 p태그 상속 */
    }}
    
    /* 4. 라디오 버튼, 슬라이더 글씨 잘 보이게 */
    .stRadio label, .stSlider label, .stNumberInput label {{
        font-size: 18px !important;
        font-weight: bold !important;
    }}
    
    /* 애니메이션들 */
    @keyframes drop {{
        0% {{ top: -10%; opacity: 1; transform: rotate(-10deg); }}
        50% {{ transform: rotate(10deg); }}
        90% {{ opacity: 1; }}
        100% {{ top: 110%; opacity: 0; transform: rotate(-10deg); }}
    }}
    {ufo_css}
    
    @keyframes wave {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-10px) rotate(2deg); }}
        100% {{ transform: translateY(0px) rotate(0deg); }}
    }}
    .ocean-container {{
        position: fixed;
        bottom: 20px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 80px;
        z-index: 998;
        animation: wave 3s infinite ease-in-out;
        opacity: 0.8;
        pointer-events: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# 차트 스타일: 아예 다크 테마로 고정
plt.style.use('dark_background')
if os.name == 'nt': 
    plt.rc('font', family='Malgun Gothic') 
    plt.rc('axes', unicode_minus=False)

# ---------------------------------------------------------
# [상태 관리] 페이지 이동
# ---------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_home(): st.session_state.page = 'home'
def go_ufo(): st.session_state.page = 'ufo'
def go_titanic(): st.session_state.page = 'titanic'

# =========================================================
# [페이지 1] 홈 화면 (메인)
# =========================================================
if st.session_state.page == 'home':
    # UFO & 파도
    for i in range(1, 11):
        st.markdown(f'<div class="ufo-{i}">🛸</div>', unsafe_allow_html=True)
    st.markdown('<div class="ocean-container">🌊🚢🌊</div>', unsafe_allow_html=True)
    
    st.write("##")
    st.write("##") 
    
    # 제목 (CSS가 적용되지만 확실하게 한 번 더 지정)
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🥱 심심할 때 해보기</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("") 
        
        if st.button("🛸 지구방위대 극비문서 : UFO 지도", use_container_width=True):
            go_ufo()
            st.rerun()
            
        st.write("") 
        
        if st.button("🚢 타이타닉 : 운명의 티켓 (생존확률)", use_container_width=True):
            go_titanic()
            st.rerun()
            
    st.markdown("<br><p style='text-align: center; color: #CCCCCC;'>위 버튼을 눌러서 시작해보세요!</p>", unsafe_allow_html=True)

# =========================================================
# [페이지 2] UFO 지도
# =========================================================
elif st.session_state.page == 'ufo':
    c_back, c_empty = st.columns([1, 8])
    with c_back:
        if st.button("⬅️ 메인으로"):
            go_home()
            st.rerun()
    
    st.title("🛸 지구방위대 극비문서: 전 세계 UFO 지도")
    st.caption("WARNING: 1급 기밀 데이터 접근 중... (Top Secret)")
    
    np.random.seed(42)
    ufo_data = pd.DataFrame({
        'lat': np.random.normal(37.09, 8, 150), 
        'lon': np.random.normal(-95.71, 15, 150),
        'type': np.random.choice(['원반형', '삼각형', '시가형', '불빛'], 150),
        'duration': np.random.randint(10, 600, 150)
    })
    
    col_map, col_stat = st.columns([3, 1])
    
    with col_map:
        layer = pdk.Layer(
            "ColumnLayer",
            data=ufo_data,
            get_position='[lon, lat]',
            get_elevation='duration',
            elevation_scale=500,
            radius=20000,
            get_fill_color='[0, 255, 0, 180]',
            pickable=True, extruded=True
        )
        view_state = pdk.ViewState(longitude=-95.71, latitude=37.09, zoom=3, pitch=50)
        
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "모양: {type}\n시간: {duration}초"},
            map_style=pdk.map_styles.DARK
        )
        st.pydeck_chart(r)
        
    with col_stat:
        st.markdown("### 👽 외계인 선호 모양")
        
        fig, ax = plt.subplots(figsize=(4, 6))
        type_counts = ufo_data['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']
        
        # 차트 그리기
        sns.barplot(data=type_counts, x='type', y='count', palette='viridis', ax=ax)
        
        # [핵심] 차트 글씨 흰색으로 강제 설정
        ax.set_ylabel("목격 횟수", color='white', fontsize=12)
        ax.set_xlabel("UFO 모양", color='white', fontsize=12)
        ax.tick_params(axis='x', colors='white', labelsize=10) # X축 눈금 흰색
        ax.tick_params(axis='y', colors='white', labelsize=10) # Y축 눈금 흰색
        
        # 테두리 제거 및 배경 투명
        sns.despine(left=True, bottom=True)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        
        st.pyplot(fig)
        st.info("데이터 분석 결과, 외계인은 미국을 좋아하는 것으로 판명되었습니다.")

    st.write("---") 
    c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
    final_text = "<div style='text-align: center; color: white;'>분석 완료!<br>수고하셨습니다 👍</div>"

    with c2: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)
    with c3: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)
    with c4: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)

# =========================================================
# [페이지 3] 타이타닉 생존 게임
# =========================================================
elif st.session_state.page == 'titanic':
    c_back, c_empty = st.columns([1, 8])
    with c_back:
        if st.button("⬅️ 메인으로"):
            go_home()
            st.rerun()
            
    st.title("🚢 타이타닉: 당신의 운명은?")
    st.markdown("##### 1912년 4월 15일, 당신은 타이타닉호에 탑승했습니다.")
    st.write("---")
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("🎫 탑승권 정보 입력")
        pclass = st.radio("객실 등급", ["1등석 (귀족)", "2등석 (중산층)", "3등석 (서민)"])
        sex = st.radio("성별", ["여성", "남성"])
        age = st.slider("나이", 1, 99, 30)
        family = st.number_input("가족 수", 0, 10, 0)
        
        st.write("")
        btn_calc = st.button("🌊 운명 확인하기", use_container_width=True)

    with col_result:
        if btn_calc:
            with st.spinner("구명보트를 찾는 중..."):
                time.sleep(1.5)
                score = 0
                if sex == "여성": score += 74
                else: score += 19
                
                if "1등석" in pclass: score += 30
                elif "2등석" in pclass: score += 10
                else: score -= 10
                
                if age < 16: score += 20
                elif age > 60: score -= 10
                
                if 1 <= family <= 3: score += 10
                elif family > 4: score -= 10

                final_prob = min(max(score, 0), 99)
                
                st.subheader("📢 생존 확률 분석 결과")
                st.progress(final_prob / 100)
                
                # 결과 글씨 크고 잘 보이게
                st.markdown(f"<h3 style='color: #00FFCC;'>생존 확률: {final_prob}%</h3>", unsafe_allow_html=True)
                
                if final_prob >= 50:
                    st.success("🎉 **생존 성공!** 구명보트에 무사히 탑승하셨습니다.")
                    st.balloons()
                else:
                    st.error("💀 **생존 실패...** 차가운 바다로 가라앉았습니다.")
                    
    st.write("---") 
    c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
    final_text = "<div style='text-align: center; color: white;'>체험 완료!<br>수고하셨습니다 👍</div>"

    with c2: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)
    with c3: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)
    with c4: 
        st.image("smile.png", use_container_width=True)
        st.markdown(final_text, unsafe_allow_html=True)