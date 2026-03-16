import sqlite3
import os

from db_config import DATA_PATH, DB_NAME


DB_FULL_PATH = os.path.join(DATA_PATH, DB_NAME)

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

def users_add(add: dict):
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

def users_get_id(user_id: int) -> dict:
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

def users_get_login(login: str) -> dict:
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

def users_update(user_id: int, update: dict):
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

def users_delete(user_id: int):
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
