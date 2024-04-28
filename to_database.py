import psycopg2

# cpt봇과의 질의응답 내용 저장
def save_chat_to_database(cur, conn, user_id, role, content, feedback=None):
    if feedback is None:
        cur.execute("INSERT INTO chat_log (user_id1, role, content) VALUES (%s, %s, %s)", (user_id, role, content))
    else:
        cur.execute("INSERT INTO chat_log (user_id1, role, content, feedback) VALUES (%s, %s, %s, %s)", (user_id, role, content, feedback))
    conn.commit()

# cpt봇 사용자 데이터 저장
def save_member_to_database(cur, conn, user_id, email, password):
    cur.execute("INSERT INTO member (user_id2, user_email, user_password) VALUES (%s, %s, %s)", (user_id, email, password))
    conn.commit()

# cpt봇 사용자 확인
def find_member_from_database(cur, user_id, password):
    cur.execute(f"SELECT user_id2, user_password FROM member WHERE user_id2 = '{user_id}' AND user_password = '{password}';")
    return cur.fetchone()