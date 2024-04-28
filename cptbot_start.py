# streamlit cloud 사용 시 필요
# import sqlite3
# import sys
# sys.modules['pysqlite3'] = sys.modules.pop('sqlite3')  # 로컬 디비

import os
import streamlit as st
import psycopg2

from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from cptbot_user_management import page1, page2
from cptbot_UI import CPT
from cptbot_intro import page0
from cptbot_guide import page3

# .env 파일 로드
load_dotenv()

# PostgreSQL 연결 설정
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)

# 커서 생성
cur = conn.cursor()

st.set_page_config(
    page_title="질의응답챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사용자를 위한 사이드바 생성
with st.sidebar:
    choice = option_menu("", ["소개","회원가입","로그인","CPT봇 이용 가이드", "CPT봇"],
    icons=['house', 'bi bi-check2-all', 'bi bi-box-arrow-in-right','book', 'bi bi-robot'],
    menu_icon="app-indicator", default_index=0,
    styles={
    "container": {"padding": "4!important", "background-color": "#fafafa"},
    "icon": {"color": "black", "font-size": "25px"},
    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
    "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

if choice == '소개':
    page0()

elif choice == "회원가입":
    success, user_id, email = page1(cur, conn)
    if success:
        #st.sidebar.success(f'{user_id}님, 회원가입이 완료되었습니다! 이메일: {email}')
        #st.write(f'{user_id}님, 회원가입이 완료되었습니다! 이메일: {email}')
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">{user_id}님, 회원가입이 완료되었습니다! 이메일: {email}</div>', unsafe_allow_html=True)

elif choice == "로그인":
    success1, user_id = page2(cur)
    if success1:
        #st.sidebar.success(f'{user_id}님, 로그인 되었습니다! 반가워요!')
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">{user_id}님, 로그인 되었습니다! 반가워요!</div>', unsafe_allow_html=True)

elif choice == 'CPT봇 이용 가이드':
    page3()

elif choice == "CPT봇":
    try:
        CPT(cur, conn)
    except KeyError:
        st.error("로그인 후 사용해주세요!!")
        st.image("./images/company_character.jpg", width=400)

cur.close()
conn.close()