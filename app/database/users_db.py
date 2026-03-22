import sqlite3
import hashlib

from config import *

'''
Users (
    id INTEGER PRIMARY KEY NOT NULL,
    role INTEGER NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
'''

class User:
    def __init__(self):
        self.id = None
        self.role = None
        self.login = None
        self.password = None

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'login': self.login
        }

def __get_hash(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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

def users_add(user: User):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            password_hash = __get_hash(user.password)

            result = cursor.execute(
                '''
                INSERT INTO users (role, login, password_hash)
                VALUES (?, ?, ?)
                ''',
                (user.role, user.login, password_hash)
            )

            return result.lastrowid

    except Exception as e:
        print(f'Ошибка добавления user: {e}')
        raise

def users_get_all():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT
                    id, role, login
                FROM Users
                '''
            )

            rows = result.fetchall()

            users = []
            for row in rows:
                user = User()
                user.id = row[0]
                user.role = row[1]
                user.login = row[2]

                users.append(user)

            return users

    except Exception as e:
        print(f'Ошибка получения users: {e}')
        raise

def users_get_id(user_id: int):
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
                user = User()

                user.id = row[0]
                user.role = row[1]
                user.login = row[2]

                return user

    except Exception as e:
        print(f'Ошибка при получении данных user: {e}')
        raise

def users_get_login(login: str):
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
                user = User()

                user.id = row[0]
                user.role = row[1]
                user.login = row[2]

                return user

    except Exception as e:
        print(f'Ошибка при получении данных user: {e}')
        raise

def users_check_password(user_id: int, password: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute(
                '''
                SELECT 
                    password_hash
                FROM Users
                WHERE id = ?
                ''',
                (user_id,)
            )

            row = res.fetchone()

            if row:
                return row[0] == __get_hash(password)

            return False

    except Exception as e:
        print(f'Ошибка проверки users: {e}')
        raise

def users_update(user: User):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                UPDATE Users
                SET 
                    role = COALESCE(?, role),
                    password_hash = COALESCE(?, password_hash)
                WHERE id = ?
                ''',
                (user.role, __get_hash(user.password), user.id)
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

def __get_all():
    with get_connection() as conn:
        cursor = conn.cursor()

        res = cursor.execute(
            '''
            SELECT * FROM Users
            '''
        )

        column_names = [dsc[0] for dsc in res.description]
        rows = res.fetchall()

        print(column_names)
        for row in rows:
            print(row)
