import sqlite3
from config import DB_FULL_PATH
import secrets
import hashlib


'''
Tokens (
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, token)
)
'''
def __get_hash(token: str):
    return hashlib.sha256(token.encode()).hexdigest()

def get_connection():
    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def tokens_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Tokens (
                    user_id INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, token)
                )
                '''
            )

    except Exception as e:
        print(f'Ошибка создания tokens: {e}')
        raise

def tokens_add_key(user_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            token = secrets.token_urlsafe(32)
            token_hash = __get_hash(token)

            res = cursor.execute(
                '''
                INSERT INTO Tokens (user_id, token)
                VALUES (?, ?)
                ''',
                (user_id, token_hash)
            )

            if res.rowcount == 1:
                return token

            return None

    except Exception as e:
        print(f'Ошибка добавления токена: {e}')
        raise

def tokens_check_key(user_id: int, token: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            token_hash = __get_hash(token)

            res = cursor.execute(
                '''
                SELECT 
                    user_id,
                    token
                FROM Tokens
                WHERE user_id = ? 
                AND token = ?
                ''',
                (user_id, token_hash)
            )

            row = res.fetchone()

            if row:
                return True

            return False

    except Exception as e:
        print(f'Ошибка получения tokens: {e}')
        raise

def tokens_delete_key(user_id: int, token: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            token_hash = __get_hash(token)

            res = cursor.execute(
                '''
                DELETE FROM Tokens
                WHERE user_id = ? AND token = ?
                ''',
                (user_id, token_hash)
            )

            return res.rowcount

    except Exception as e:
        print(f'Ошибка удаления tokens: {e}')
        raise

def tokens_delete_all_keys(user_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute(
                '''
                DELETE FROM Tokens
                WHERE user_id = ? 
                ''',
                (user_id,)
            )

            return res.rowcount

    except Exception as e:
        print(f'Ошибка удаления tokens: {e}')
        raise

def __get_all():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute(
                '''
                SELECT * FROM Tokens
                '''
            )

            column_names = [dsc[0] for dsc in res.description]
            rows = res.fetchall()

            print(column_names)
            for row in rows:
                print(row)

    except Exception as e:
        print(f'Ошибка: {e}')
        raise


