import streamlit as st

def page0():
    # 사용자가 선택할 수 있는 탭을 selectbox로 표시합니다.
    tab2, tab1 = st.tabs(["챗봇 소개", "회사 소개"])
    with tab1:
        st.image("./images/company_logo.jpg", use_column_width=True)

# HTML과 CSS를 이용하여 텍스트를 가운데 정렬하고, 글씨를 두껍게 하며, 이모티콘을 포함
        st.markdown("""
    <style>
    .centered-bold {
        text-align: center;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
    <div class="centered-bold">
        🏆 1위 교육·출판 전문 기업 🏆
    </div>
    """, unsafe_allow_html=True)


# HTML을 사용하여 텍스트를 가운데 정렬
    #     st.markdown("""
    # <style>
    # .centered-normal {
    #     text-align: center;
    #     font-weight: normal; /* 더 얇은 글씨체 */
    #     font-size: 24px; /* 더 작은 글씨 크기 */
    # }
    # </style>
    # <div class="centered-normal">
    #     💡 교육의 미래를 선도합니다. 💡
    # </div>
    # """, unsafe_allow_html=True)

        st.markdown('---')
        st.write("천재교육은 교육 서비스에 최적화된 대한민국 1등 교육·출판 전문 기업입니다.")
        st.write("")
        st.write("천재교육은 제5차 교육과정부터 국정·검정·인정 교과용 도서를 개발, 발행하고 연간 3,700여 종에 이르는 유아동·초·중·고등 학습 교재를 발간하고 있습니다. 또한 미래 인재 육성을 위한 학원 프랜차이즈 사업, 4차 산업혁명 시대에 발맞춘 스마트러닝, 에듀테크 사업 등을 통해 대한민국 교육 트렌드를 주도하고 있습니다.")
        st.markdown('---')
        

    with tab2:
        st.image("./images/cptbot_intro.jpg", use_column_width=True)
    #     st.markdown("""
    # <style>
    # .centered-bold-two {
    #     text-align: center;
    #     font-weight: bold;
    #     font-size: 48px;
    # }
    # </style>
    # <div class="centered-bold">
    #     🧑‍🏫 파이썬 튜터링 챗봇 런칭 🧑‍🏫
    # </div>
    # """, unsafe_allow_html=True)
        
        st.markdown("""
    <style>
    .centered-normal {
        text-align: center;
        font-weight: bold; /* 굵은 글씨체 */
        font-size: 24px; /* 더 작은 글씨 크기 */
        white-space: nowrap; /* 텍스트를 한 줄로 표시 */
        overflow: hidden; /* 텍스트가 넘칠 경우 숨김 */
        text-overflow: ellipsis; /* 넘친 텍스트를 ...으로 표시 */
    }
    </style>
    <div class="centered-normal">
        🧑‍🏫 당신만을 위한 파이썬 선생님 🧑‍🏫
    </div>
    """, unsafe_allow_html=True)
        # st.subheader("당신만을 위한 파이썬 선생님!")
        st.markdown('---')
        st.write("질문을 하면 답(코드)만 알려주는 챗봇은 학습 효과를 저해합니다. 천재교육은 AI 기술의 발전 속에 진정한 '학습'을 위한 챗봇을 만들고자 하였습니다.")
        st.write("CPT, 학습자의 논리력과 사고력을 향상할 수 있는 챗봇! 지금 시작합니다.")
        st.markdown('---')