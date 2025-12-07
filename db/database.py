import os
import psycopg2
import json

conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

def get_user_state(chat_id):
    cur = conn.cursor()
    cur.execute("SELECT state FROM user_state WHERE chat_id = %s", (chat_id,))
    row = cur.fetchone()
    return row[0] if row else None

def save_user_state(chat_id, state):
    cur = conn.cursor()
    if state is None:
        cur.execute("DELETE FROM user_state WHERE chat_id=%s", (chat_id,))
    else:
        cur.execute("""
            INSERT INTO user_state (chat_id, state)
            VALUES (%s, %s)
            ON CONFLICT (chat_id)
            DO UPDATE SET state = EXCLUDED.state
        """, (chat_id, json.dumps(state)))
    conn.commit()

def save_appointment_db(state):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appointments (chat_id, service, date, time)
        VALUES (%s, %s, %s, %s)
    """, (
        state.get("chat_id", 0),
        state["service"],
        state["date"],
        state["time"]
    ))
    conn.commit()

