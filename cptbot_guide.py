import streamlit as st

def page3():

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
        <h1 class="login-text">CPT봇 이용 가이드</h1>
        """, unsafe_allow_html=True)

        st.write("1. 사용자의 최적화된 정보 제공을 위해 먼저 로그인을 해주세요")
        st.write("2. '파이썬으로 00하는 법 알려줘'의 형태로 질문하면 더욱 정확한 답변을 확인할 수 있습니다.")
        st.write("3. 힌트는 총 2단계로 제공됩니다. 첫 번째 힌트에서는 코드를 짜기 위한 간단한 논리 구조를 설명해줍니다. 여기서 추가적인 힌트가 필요하면 [힌트 한 번 더 볼래요:bulb:] 버튼을 눌러주세요.\
                 그럼 첫 번째 힌트에서 알려준 논리 구조에 대한 상세 설명을 확인할 수 있습니다.")
        st.write("4. 추가적인 힌트가 필요 없다면 [정답 코드를 알고 싶어요:heavy_check_mark:] 버튼을 눌러주세요.")
        st.write("5. 정답 코드 확인 후, 피드백 버튼을 통해 응답 평가를 하면 더욱 더 최적화된 서비스를 제공 받을 수 있습니다.")