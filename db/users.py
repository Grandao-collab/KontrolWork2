import sqlite3
from config import DB_NAME
from db.queries import INSERT_USER

def register_user(tg_id: int, username: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(INSERT_USER, (tg_id, username))
        conn.commit()