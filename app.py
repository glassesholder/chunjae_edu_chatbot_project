import sqlite3
from dotenv import load_dotenv
import sys
sys.modules['pysqlite3'] = sys.modules.pop('sqlite3')
import streamlit as st
import os

from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain





st.set_page_config(
    page_title="행복한 코딩봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# .env 파일 로드
load_dotenv()

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


st.subheader('너의 질문을 적어줘!')


def generate_response(input_text):
  result = chain(input_text)
  return result['answer']

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕 나는 코딩 챗봇이야! 무엇을 도와줄까?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg =  generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


