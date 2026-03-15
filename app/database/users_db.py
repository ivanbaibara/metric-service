import sqlite3
import os
from db_config import DATA_PATH, BD_NAME


DB_FULL_PATH = os.path.join(DATA_PATH, BD_NAME)

'''
Users (
    id INTEGER PRIMARY KEY NOT NULL,
    role INTEGER NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    description TEXT 
)
'''

def get_connection():
    return sqlite3.connect(DB_FULL_PATH)

# Создание таблицы Users (если нет)
def users_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY NOT NULL,
                        role INTEGER NOT NULL,
                        login TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        description TEXT 
                    )
                    ''')
    except Exception as e:
        print(f'Ошибка при создании таблицы users: {e}')
        raise

# Добавление пользователя
def user_add():
    ...

# Получение информации о пользователе
def user_get():
    ...

# Обновление информации о пользователе
def user_update():
    ...

# Удаление пользователя
def user_delete():
    ...
