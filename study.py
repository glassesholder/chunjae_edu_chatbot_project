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

create_query = "CREATE TABLE chat_logs1 (id SERIAL PRIMARY KEY, role VARCHAR(50), content TEXT);"

insert_query = "INSERT INTO chat_logs1 (role, content) VALUES ( 'system1', '안녕하세요1');"

cursor.execute(create_query)
cursor.execute(insert_query)
db.commit()

# 잘 되는 것을 확인하였다.
