# Создание таблиц
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    tg_id INTEGER PRIMARY KEY,
    username TEXT
);
"""

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    is_done INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(tg_id)
);
"""

# Пользователи
INSERT_USER = "INSERT OR IGNORE INTO users (tg_id, username) VALUES (?, ?);"

# Задачи
INSERT_TASK = "INSERT INTO tasks (user_id, title) VALUES (?, ?);"

SELECT_USER_TASKS = """
SELECT t.id, t.title, t.is_done 
FROM tasks t
INNER JOIN users u ON t.user_id = u.tg_id
WHERE u.tg_id = ?;
"""

SELECT_TASK_BY_ID = "SELECT user_id, is_done FROM tasks WHERE id = ?;"

UPDATE_TASK_DONE = "UPDATE tasks SET is_done = 1 WHERE id = ? AND user_id = ?;"

DELETE_TASK = "DELETE FROM tasks WHERE id = ? AND user_id = ?;"

# Статистика
SELECT_STATS = """
SELECT 
    COUNT(id) as total,
    SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) as done,
    SUM(CASE WHEN is_done = 0 THEN 1 ELSE 0 END) as undone
FROM tasks
WHERE user_id = ?
GROUP BY user_id;
"""