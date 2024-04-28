import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


# database connection 생성
db = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)

# 커서 생성 > 특정 SQL 문장을 처리한 결과를 담고 있는 영역을 가리키는 일종의 포인터 / 쿼리문에 의해서 반환되는 결과값들을 저장하는 메모리공간
cursor = db.cursor()

# 사용자 정보 저장 테이블, 사용자 질의응답 내용 저장 테이블 생성 및 연결
create_query1 = "CREATE TABLE member (user_id2 TEXT PRIMARY KEY, user_email TEXT NOT NULL, user_password TEXT NOT NULL);"
create_query2 = "CREATE TABLE chat_log (user_id1 TEXT REFERENCES member(user_id2), role TEXT, content TEXT, feedback TEXT);"


cursor.execute(create_query1)
cursor.execute(create_query2)
db.commit()

# 테이블 생성이 잘 되는 것을 확인하였다.
