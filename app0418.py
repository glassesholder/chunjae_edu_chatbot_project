# import sqlite3
# import sys
# sys.modules['pysqlite3'] = sys.modules.pop('sqlite3')  # 로컬 디비

import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from dotenv import load_dotenv
import streamlit as st
import os
import psycopg2  # PostgreSQL 라이브러리 추가


from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


# .env 파일 로드
load_dotenv()

# 환경 변수 설정
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

#PostgreSQL 연결 설정
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)

# 커서 생성
cur = conn.cursor()

create_query = "CREATE TABLE chat_json (role TEXT, content TEXT);"

cur.execute(create_query)
conn.commit()

def save_chat_to_database(role, content):
    cur.execute("INSERT INTO chat_json (role, content) VALUES (%s, %s)", (role, content))
    conn.commit()


st.set_page_config(
    page_title="질의응답챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        width: 70%; /* 너비를 조정하여 대화창을 넓게 설정합니다 */
        padding: 20px;
        background-color: #f4f4f4;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
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


st.title("💚cpt bot💚")

st.caption('CPT(Chunjae Python Tutor) BOT은 GPT-3.5를 학습시킨 결과로 응답을 제공합니다.')

st.divider()
st.header('천재교육은 너의 질문을 환영해!')
st.markdown(":red[파이썬으로 00하는 방법이 궁금해.] 또는 :red[00하는 코드를 만들고 싶어.]와 같이 질문해 주세요!")



# PDF 파일 로드 및 텍스트 추출
loader = PyPDFLoader('train2.pdf')
documents = loader.load()
# 텍스트를 적절한 크기로 나누기
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
# # 문장을 벡터로 변환
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
# 챗봇 설정
system_template_hint = """당신은 중등 정보(컴퓨터) 과목 선생님입니다.
사용자는 중학교 또는 고등학교의 정규교과과정을 통해 지금 파이썬을 기초부터 학습하고 있습니다.
당신은 사용자의 질문에 단계적 해결 방법을 제시해야 합니다.
답변에 코드를 절대 포함해서는 안됩니다.
파이썬관련 질문이 들어오면 절대 코드를 답변하지 않고,
코드를 작성하는 사고와 논리를 알려주세요.
----------------
{summaries}
You MUST answer in Korean and in Markdown format:"""
messages_hint = [
    SystemMessagePromptTemplate.from_template(system_template_hint),
    HumanMessagePromptTemplate.from_template("{question}")
]

prompt_hint = ChatPromptTemplate.from_messages(messages_hint)
chain_type_kwargs_hint = {"prompt": prompt_hint}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
chain_hint = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs_hint
)
# 챗봇 설정
system_template_answer = """당신은 중등 정보(컴퓨터) 과목 선생님입니다.
사용자는 중학교 또는 고등학교의 정규교과과정을 통해 지금 파이썬을 기초부터 학습하고 있습니다.
당신은 사용자의 질문에 정답 코드만 제시해야 합니다.
파이썬관련 질문이 들어오면 절대 설명하지 않고,
코드만 알려주세요.
----------------
{summaries}
You MUST answer in Korean and in Markdown format:"""

messages_answer = [
    SystemMessagePromptTemplate.from_template(system_template_answer),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt_answer = ChatPromptTemplate.from_messages(messages_answer)
chain_type_kwargs_answer = {"prompt": prompt_answer}

chain_answer = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs_answer
)

# 여기에 나머지 코드 부분이 옵니다...
def generate_response_hint(input_text):
    result = chain_hint(input_text)
    return result['answer']
def generate_response_answer(input_text):
    result = chain_answer(input_text)
    return result['answer']

# Streamlit 앱 시작
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕 나는 코딩 챗봇이야! 무엇을 도와줄까?"}]
    #save_chat_to_database("assistant", "안녕 나는 코딩 챗봇이야! 무엇을 도와줄까?")
if "last_question" not in st.session_state:
    st.session_state["last_question"] = ""  # 직전 질문을 저장할 공간


# 맨처음에 아무것도 안적었을때 UI
#for msg in st.session_state.messages:
#    st.chat_message(msg["role"]).write(msg["content"])


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        if "```" in msg['content']:
            st.chat_message("assistant").write(msg['content'])
        else:
            st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)


# 이전 대화 가져와서 채팅창에 표시(즉, 그 전에 있던 것)
if prompt := st.chat_input():  # 만약 사용자가 입력한 내용이 있다면 
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-container"><div class="user-msg">{prompt}</div></div>', unsafe_allow_html=True)
    save_chat_to_database("user", prompt)

    msg = generate_response_hint(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg}</div></div>', unsafe_allow_html=True)
    save_chat_to_database('assistant', msg)
    st.session_state["last_question"] = msg # 직전 질문 저장

# CSS 스타일을 정의합니다.
button_style = """
    <style>
        .stButton>button {
            width: 400px;
        }
    </style>
"""
# CSS 스타일을 Streamlit에 적용합니다.
st.markdown(button_style, unsafe_allow_html=True)



# "힌트 한번 더" 버튼 로직
if st.button("힌트 한 번 더 볼래요!"):
    if st.session_state["last_question"]:  # 직전 질문이 있을 경우에만 작동
        prompt = st.session_state["last_question"]  # 직전 질문을 다시 사용
        save_chat_to_database("user", "힌트 한번 더 볼래요!")
        msg = generate_response_hint(prompt + ' 조금 더 자세하게 알려줘.')  # 직전 질문에 대한 답변(힌트) 생성
        st.session_state.messages.append({"role": "assistant", "content": msg})
        save_chat_to_database("assistant", msg)
        st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container"><div class="assistant-msg">{"직전에 질문이 없습니다."}</div></div>', unsafe_allow_html=True)


if st.button("정답 코드를 알고 싶어요!"):
    if st.session_state["last_question"]:  # 직전 질문이 있을 경우에만 작동
        prompt = st.session_state["last_question"]  # 직전 질문을 다시 사용
        save_chat_to_database("user", "정답 코드를 알고 싶어요!")
        msg = generate_response_answer(prompt)  # 직전 질문에 대한 답변(힌트) 생성
        st.session_state.messages.append({"role": "assistant", "content": msg})
        save_chat_to_database("assistant", msg)
        st.chat_message("assistant").write(msg)
    else:
        st.markdown(f'<div class="chat-container"><div class="assistant-msg">{"직전에 질문이 없습니다."}</div></div>', unsafe_allow_html=True)



# 연결 및 커서 닫기
cur.close()
conn.close()
