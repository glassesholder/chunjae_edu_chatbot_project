# CREATE TABLE chat_logs (
#     id SERIAL PRIMARY KEY,
#     role VARCHAR(50),
#     content TEXT
# );
# 사전에 만들어 놓는 것을 추천, study.py 참고

from dotenv import load_dotenv
import streamlit as st
import os
import psycopg2  # PostgreSQL 라이브러리 추가

from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

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

# 사용자와 챗봇 대화를 PostgreSQL에 저장하는 함수
def save_chat_to_database(role, content):
    cur.execute("INSERT INTO chat_logs (role, content) VALUES (%s, %s)", (role, content))
    conn.commit()

st.set_page_config(
    page_title="행복한 코딩봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 환경 변수 설정
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")

loader = PyPDFLoader('train2.pdf')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template="""당신은 중등 정보(컴퓨터) 과목 선생님입니다.
사용자는 파이썬을 기초부터 학습하는 학습자입니다.
당신은 사용자의 질문에 단계적 해결 방법을 제시해야 합니다.
답변에 코드를 절대 포함해서는 안됩니다.
파이썬관련 질문이 들어오면 절대 코드를 답변하지 않고,
코드를 작성하는 사고와 논리를 알려주세요.
----------------
{summaries}

You MUST answer in Korean and in Markdown format:"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]

prompt = ChatPromptTemplate.from_messages(messages)


chain_type_kwargs = {"prompt": prompt}

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)  # Modify model_name if you have access to GPT-4

chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever = retriever,
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
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
        background-color: #ffeb3b;
        color: #333;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    
    /* 챗봇 메시지 스타일링 */
    .assistant-msg {
        background-color: #4caf50;
        color: white;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💚cpt-bot💚")

st.subheader('천재교육은 너의 질문을 환영해!')


def generate_response(input_text):
  result = chain(input_text)
  return result['answer']

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕 나는 코딩 챗봇이야! 무엇을 도와줄까?"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-container"><div class="user-msg">{prompt}</div></div>', unsafe_allow_html=True)
    save_chat_to_database("user", prompt)  # 사용자 입력을 데이터베이스에 저장

    # 챗봇 응답 생성 및 저장
    msg = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.markdown(f'<div class="chat-container"><div class="assistant-msg">{msg}</div></div>', unsafe_allow_html=True)
    save_chat_to_database("assistant", msg)  # 챗봇 응답을 데이터베이스에 저장

# 연결 및 커서 닫기
cur.close()
conn.close()
