import streamlit as st
import random 
import datetime 

st.title("로또 번호 생성기")

def generate_lotto():
    lotto=set()
    while len(lotto)<=6:
        number=random.randint(1,46) #range(1,46)으로 해야함
        lotto.add(number) #set은 append가 안된다?

    return lotto

button=st.button("로또 번호를 생성해주세요!")
if button:
    for i in range(1,6): #6을 해야 5개를 찍어준다.
        st.subheader(f"{i}번째 추천 로또 번호: {generate_lotto()}")
    st.write(f"생성된 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 구분선
st.write("---")

# 1. 화면을 3개의 기둥(칼럼)으로 나눕니다. [비율 1 : 1 : 1]
col1, col2, col3 = st.columns([1, 1, 1])

# 2. 그중 '가운데 기둥(col2)'에만 내용을 넣습니다.
with col2:
    st.image("smile.png", caption="🍀 Good Luck 🍀", width=200)