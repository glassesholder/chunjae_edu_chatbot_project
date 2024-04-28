import streamlit as st
import re
from to_database import save_member_to_database, find_member_from_database

def validate_password(password):
    # 비밀번호는 최소 8자 이상이어야 하며, 특수 문자 중 하나를 포함해야 합니다.
    if len(password) < 8:
        return False
    if re.search(r'[!@#$]', password) is None:
        return False
    return True

# page1 : 회원가입
def page1(cur, conn):
    col1, col2 = st.columns([1,16])

    with col1:
        # 이미지 크기를 조정하여 컬럼에 맞게 조화롭게 표시
        st.image("./images/chatbot.png", width=64)  # 이미지의 width를 조정

    with col2:
        # HTML과 CSS를 사용하여 글자 간격 조정
        st.markdown("""
        <style>
        .login-text {
            margin-top: -10px;  # 글자 간격 조정
        }
        </style>
        <h1 class="login-text">회원가입</h1>
        """, unsafe_allow_html=True)






    # st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">사용자 정보를 각 설명에 맞게 정보를 입력해주세요.', unsafe_allow_html=True)
    st.markdown("---")
    # 사용자 정보 입력
    user_id = st.text_input('사용자 ID')
    email = st.text_input('이메일')
    password = st.text_input('사용자 PW', type='password')
    confirm_password = st.text_input('사용자 PW 확인', type='password')
    
    

    # 이메일 형식 확인
    if '@' not in email:
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">이메일 형식을 확인해주세요.', unsafe_allow_html=True)
        return False, None, None

    # 비밀번호 일치 여부 확인
    if password != confirm_password:
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">비밀번호가 일치하지 않습니다. 다시 입력해주세요.', unsafe_allow_html=True)
        return False, None, None
    
    # 비밀번호 유효성 검사
    if not validate_password(password):
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">비밀번호는 최소 8자 이상이어야 하며, 특수 문자 중 하나를 포함해야 합니다.', unsafe_allow_html=True)
        return False, None, None
    cur.execute("SELECT user_id2 FROM member")
    user_id2 = [row[0] for row in cur.fetchall()]

    # 이메일 목록 조회
    cur.execute("SELECT user_email FROM member")
    user_email = [row[0] for row in cur.fetchall()]
    
    if user_id in user_id2:
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">이미 존재하는 아이디입니다.', unsafe_allow_html=True)
        return False, None, None
    if email in user_email:
        st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">이미 존재하는 이메일입니다.', unsafe_allow_html=True)
        return False, None, None

    # 회원가입 버튼 클릭 여부 확인
    if st.button('회원가입'):
        save_member_to_database(cur, conn, user_id, email, password)
        return True, user_id, email
    else:
        return False, None, None

# page2 : 로그인
def page2(cur):

    

    col1, col2 = st.columns([1,16])

    with col1:
        # 이미지 크기를 조정하여 컬럼에 맞게 조화롭게 표시
        st.image("./images/chatbot.png", width=64)  # 이미지의 width를 조정

    with col2:
        # HTML과 CSS를 사용하여 글자 간격 조정
        st.markdown("""
        <style>
        .login-text {
            margin-top: -10px;  # 글자 간격 조정
        }
        </style>
        <h1 class="login-text">로그인</h1>
        """, unsafe_allow_html=True)



    
    st.subheader('사용자 ID, PW를 입력해주세요.')

    # 사용자 정보 입력
    user_id = st.text_input('사용자 ID')
    password = st.text_input('사용자 PW', type='password')
    
    cur.execute("SELECT user_id2 FROM member")
    user_id2 = [row[0] for row in cur.fetchall()]

    # 비밀번호 목록 조회
    cur.execute("SELECT user_password FROM member WHERE user_id2=%s", (user_id,))
    password2 = [row[0] for row in cur.fetchall()]
    
    # 회원가입 버튼 클릭 여부 확인
    if st.button('로그인'):
        if find_member_from_database(cur, user_id, password)==None:
            if user_id not in user_id2:
                st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">존재하지 않는 아이디입니다.', unsafe_allow_html=True)
                return False, None
            elif password not in password2:
                st.write(f'<div style="background-color: #aaf0d1; padding: 10px; border-radius: 5px;">잘못된 비밀번호입니다.', unsafe_allow_html=True)
                return False, None
        else:
            user_id = find_member_from_database(cur, user_id, password)[0]
            st.session_state['user_id'] = user_id
            return True, user_id
    else:
        return False, None