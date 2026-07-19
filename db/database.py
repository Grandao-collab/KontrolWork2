import sqlite3
from config import DB_NAME
from db.queries import CREATE_USERS_TABLE, CREATE_TASKS_TABLE

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_TASKS_TABLE)
        conn.commit()