import os
import streamlit as st
from streamlit_pills import pills

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from to_database import save_chat_to_database


#기본적인 chatbot ui를 위한 style 작성
def CPT(cur, conn):
    st.markdown(
    """
    <style>
    body {
        background-color: #b3e5fc; /* 연한 하늘색 배경 */
    }
    /* 전체 챗봇 창 가운데 정렬 */
    .full-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    /* 챗봇 창 스타일링 */
    .chat-container {
        width: 90%; /* 너비를 조정하여 대화창을 넓게 설정합니다 */
        padding: 20px;
        background-color: #f4f4f4;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .chat-container2 {
        width: 90%; /* 너비를 조정하여 대화창을 넓게 설정합니다 */
        padding: 20px;
        background-color: #f4f4f4;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        float: right;
    }
    
    /* 사용자 메시지 스타일링 */
    .user-msg {
        background-color: #fff9c4;
        color: #333;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    
    /* 챗봇 메시지 스타일링 */
    .assistant-msg {
        background-color: #aaf0d1;
        color: black;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

    # PDF 파일 로드 및 텍스트 추출
    loader = PyPDFLoader('./files/train.pdf')
    documents = loader.load()

    # 텍스트를 적절한 크기로 나누기
    text_splitter = CharacterTextSplitter(chunk_size=1, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # 문장을 벡터로 변환한 뒤, vector_store에 저장
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(texts, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    # 사고력을 기르기 위한 챗봇 system_prompt 설정
    system_template_hint = """당신은 중등 정보(컴퓨터) 과목 선생님입니다.
    사용자는 중학교 또는 고등학교의 정규교과과정을 통해 지금 파이썬을 기초부터 학습하고 있습니다.
    당신은 사용자의 질문에 단계적 해결 방법을 제시해야 합니다.
    답변에 코드를 절대 포함해서는 안됩니다.
    파이썬관련 질문이 들어오면 절대 코드를 답변하지 않고,
    코드를 작성하는 사고와 논리를 알려주세요.
    가독성을 위해 힌트는 한줄씩,번호를 매겨 알려주세요.
    
    ----------------
    {summaries}
    You MUST answer in Korean and in Markdown format:"""
    messages_hint = [
        SystemMessagePromptTemplate.from_template(system_template_hint),
        HumanMessagePromptTemplate.from_template("{question}")
    ]

    prompt_hint = ChatPromptTemplate.from_messages(messages_hint)
    chain_type_kwargs_hint = {"prompt": prompt_hint}
    llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0125:text-analysis::9FGo0Rf4", temperature=0)

    #사고력을 기르기 위한 챗봇 생성
    chain_hint = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs_hint
    )

    # 정답 코드 제공을 위한 챗봇 system_prompt 설정
    system_template_answer = """당신은 중등 정보(컴퓨터) 과목 선생님입니다.
    사용자는 중학교 또는 고등학교의 정규교과과정을 통해 지금 파이썬을 기초부터 학습하고 있습니다.
    당신은 사용자의 질문에 오직 정답 python 코드만 제시해야 합니다.
    파이썬관련 질문이 들어오면 절대 한글로 설명하지 않고,
    python 코드만 알려줘서 학습을 도와주세요.
    예시 코드가 필요하다면 예시코드까지 제공해주세요.
    ----------------
    {summaries}
    You MUST answer in python code : """

    messages_answer = [
        SystemMessagePromptTemplate.from_template(system_template_answer),
        HumanMessagePromptTemplate.from_template("{question}")
    ]

    prompt_answer = ChatPromptTemplate.from_messages(messages_answer)
    chain_type_kwargs_answer = {"prompt": prompt_answer}

     # 정답 코드 제공을 위한 챗봇 생성
    chain_answer = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs_answer
    )
    user_id = st.session_state['user_id']

    def generate_response_hint(input_text):
        result = chain_hint(input_text)
        return result['answer']
    def generate_response_answer(input_text):
        result = chain_answer(input_text)
        return result['answer']

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
        <h1 class="login-text">CPT(Chunjae Python Tutor)</h1>
        """, unsafe_allow_html=True)

    st.caption('CPT(Chunjae Python Tutor)봇은 GPT-3.5를 학습시킨 결과로 응답을 제공합니다.')
    st.divider()
    st.header(f'{user_id}님, 반가워요:wave:')
    # st.markdown(":red[파이썬으로 00하는 방법이 궁금해.] 또는 :red[00하는 코드를 만들고 싶어.]와 같이 질문해 주세요!")
    
    # cpt봇이 말해주는 첫 문장 생성
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "궁금증 해결사 CPT봇이에요! 무엇을 도와드릴까요?"}]
        save_chat_to_database(cur, conn, user_id ,"assistant", "궁금증 해결사 CPT봇이에요! 무엇을 도와드릴까요?")
    
    # cpt봇이 응답한 직전 응답을 저장할 공간
    if "last_question" not in st.session_state:
        st.session_state["last_question"] = ""

    # cpt봇과 나눈 이전 대화 가져와서 채팅창에 표시(즉, 그 전에 있던 것)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-container2"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            if "```" in msg['content']:
                st.chat_message("assistant").write(msg['content'])
            else:
                st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)

    # 사용자 질문과 그에 따른 응답 출력
    if prompt := st.chat_input("파이썬으로 00하는 법 알려줘"):  # 만약 사용자가 입력한 내용이 있다면 
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-container2"><div class="user-msg">{prompt}</div></div>', unsafe_allow_html=True)
        save_chat_to_database(cur, conn, user_id, "user", prompt)
        with st.spinner('답변을 생성 중입니다💨'):
            msg = generate_response_hint(prompt)

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg}</div></div>', unsafe_allow_html=True)

        st.session_state["last_question"] = msg # 직전 질문 저장
        selected = pills("Feedback please", ["만족해요", "스타일이 마음에 안 들어요", "이해가 안 돼요", "코드가 틀렸어요"], ["👍", "👎", "❓", "❌"], index=False)
        save_chat_to_database(cur, conn, user_id, 'assistant', msg, selected)

    # 버튼을 위한 CSS 스타일을 정의합니다.
    button_style = """
        <style>
            .stButton>button {
                width: 60%;
            }
        </style>
    """

    # CSS 스타일을 Streamlit에 적용합니다.
    st.markdown(button_style, unsafe_allow_html=True)

    # "힌트 한 번 더 볼래요" 버튼 로직
    if st.button("힌트 한 번 더 볼래요:bulb:"):
        if st.session_state["last_question"]:  # 직전 질문이 있을 경우에만 작동
            prompt = st.session_state["last_question"]  # 직전 질문을 다시 사용
            st.session_state.messages.append({"role": "user", "content":  "힌트 한 번 더 볼래요!"})
            save_chat_to_database(cur, conn, user_id, "user", "힌트 한 번 더 볼래요!")
            with st.spinner('답변을 생성 중입니다💨'):
                msg = generate_response_hint(prompt + ' 조금 더 자세하게 알려줘.')  # 직전 질문에 대한 답변(힌트) 생성

            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state["last_question"] = msg


            st.markdown(f'<div class="chat-container2"><div class="user-msg">{"힌트 한 번 더 볼래요!"}</div></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg}</div></div>', unsafe_allow_html=True)
            selected = pills("Feedback please", ["만족해요", "스타일이 마음에 안 들어요", "이해가 안 돼요", "코드가 틀렸어요"], ["👍", "👎", "❓", "❌"], index=False)
            save_chat_to_database(cur, conn, user_id, "assistant", msg, selected)
        else:
            st.markdown(f'<div class="chat-container"><div class="assistant-msg">{"직전에 질문이 없습니다."}</div></div>', unsafe_allow_html=True)

    # "정답 코드를 알고 싶어요" 버튼 로직
    if st.button("정답 코드를 알고 싶어요:heavy_check_mark:"):
        if st.session_state["last_question"]:  # 직전 질문이 있을 경우에만 작동
            prompt = st.session_state["last_question"]  # 직전 질문을 다시 사용
            st.session_state.messages.append({"role": "user", "content":  "정답 코드를 알고 싶어요!"})
            save_chat_to_database(cur, conn, user_id, "user", "정답 코드를 알고 싶어요!")

            with st.spinner('답변을 생성 중입니다💨'):
                msg = generate_response_answer(prompt)  # 직전 질문에 대한 답변(힌트) 생성
            st.session_state.messages.append({"role": "assistant", "content": msg})


            st.markdown(f'<div class="chat-container2"><div class="user-msg">{"정답 코드를 알고 싶어요!"}</div></div>', unsafe_allow_html=True)
            st.chat_message("assistant").write(msg)
            selected = pills("Feedback please", ["만족해요", "스타일이 마음에 안 들어요", "이해가 안 돼요", "코드가 틀렸어요"], ["👍", "👎", "❓", "❌"], index=False)
            save_chat_to_database(cur, conn, user_id, "assistant", msg, selected)
        else:
            st.markdown(f'<div class="chat-container"><div class="assistant-msg">{"직전에 질문이 없습니다."}</div></div>', unsafe_allow_html=True)