import sqlite3
import os

from db_config import DATA_PATH, BD_NAME


DB_FULL_PATH = os.path.join(DATA_PATH, BD_NAME)

'''
Users (
    id INTEGER PRIMARY KEY NOT NULL,
    role INTEGER NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
'''

def get_connection():
    return sqlite3.connect(DB_FULL_PATH)

# Создание таблицы Users (если нет)
def users_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY NOT NULL,
                        role INTEGER NOT NULL,
                        login TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )
                '''
            )

    except Exception as e:
        print(f'Ошибка при создании таблицы users: {e}')
        raise

# Добавление пользователя
def user_add(add: dict):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                INSERT INTO users (role, login, password_hash)
                VALUES (?, ?, ?)
                ''',
                (add['role'], add['login'], add['password_hash'])
            )

            return result.lastrowid

    except Exception as e:
        print(f'Ошибка добавления user: {e}')
        raise

# Получение информации о пользователе через id
def user_get_id(user_id: int) -> dict:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT
                    id, role, login, password_hash
                FROM Users
                WHERE id = ?
                ''',
                (user_id,)
            )

            row = result.fetchone()
            if row:
                return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'password_hash': row[3]
                }
            return {}

    except Exception as e:
        print(f'Ошибка при получении данных user: {e}')
        raise

# Получение информации о пользователе через login
def user_get_login(login: str) -> dict:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT
                    id, role, login, password_hash
                FROM Users
                WHERE login = ?
                ''',
                (login,)
            )

            row = result.fetchone()
            if row:
                return {
                    'id': row[0],
                    'role': row[1],
                    'login': row[2],
                    'password_hash': row[3]
                }
            return {}

    except Exception as e:
        print(f'Ошибка при получении данных user: {e}')
        raise

# Обновление информации о пользователе
def user_update(user_id: int, update: dict):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                UPDATE Users
                SET 
                    role = COALESCE(?, role),
                    login = COALESCE(?, login),
                    password_hash = COALESCE(?, password_hash)
                WHERE id = ?
                ''',
                (update['role'], update['login'], update['password_hash'], user_id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка обновления user: {e}')
        raise

# Удаление пользователя
def user_delete(user_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Users WHERE id = ?
                ''',
                (user_id, )
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка удаления user: {e}')
        raise
