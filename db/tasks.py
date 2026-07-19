import sqlite3
from config import DB_NAME
from db import queries

def add_task(user_id: int, title: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.INSERT_TASK, (user_id, title))
        conn.commit()

def get_tasks(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_USER_TASKS, (user_id,))
        return cursor.fetchall()  # Возвращает список кортежей [(id, title, is_done), ...]

def get_task_info(task_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_TASK_BY_ID, (task_id,))
        return cursor.fetchone()

def complete_task(task_id: int, user_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Проверяем, существует ли задача и принадлежит ли пользователю
        task = get_task_info(task_id)
        if not task or task[0] != user_id:
            return False
        
        cursor.execute(queries.UPDATE_TASK_DONE, (task_id, user_id))
        conn.commit()
        return True

def delete_task(task_id: int, user_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        task = get_task_info(task_id)
        if not task or task[0] != user_id:
            return False
            
        cursor.execute(queries.DELETE_TASK, (task_id, user_id))
        conn.commit()
        return True

def get_user_stats(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_STATS, (user_id,))
        return cursor.fetchone()