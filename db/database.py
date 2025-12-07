import os
import psycopg2
import json
from urllib.parse import urlparse

# Railway DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse da URL
url = urlparse(DATABASE_URL)

# Conexão com SSL obrigatório
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
    sslmode="require"
)

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
        """, (chat_id, json.dum_

