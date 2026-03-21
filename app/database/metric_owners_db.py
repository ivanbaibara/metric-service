import sqlite3

from config import *


'''
Metric_Owners (
    user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    metric_id INTEGER NOT NULL REFERENCES Metrics(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, metric_id)
)
'''


def get_connection():
    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def metric_owners_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Metric_Owners (
                    user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                    metric_id INTEGER NOT NULL REFERENCES Metrics(id) ON DELETE CASCADE,
                    PRIMARY KEY (user_id, metric_id)
                )
                '''
            )

    except Exception as e:
        print(f'Ошибка создания metric_owners: {e}')
        raise

def metric_owners_add(user_id: int, metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                INSERT INTO Metric_Owners (user_id, metric_id)
                VALUES (?, ?)
                ''',
                (user_id, metric_id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка добавления metric_owners: {e}')
        raise

def metric_owners_get_all_metrics(user_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            results = cursor.execute(
                '''
                SELECT metric_id
                FROM Metric_Owners
                WHERE user_id = ?
                ''',
                (user_id, )
            )

            rows = results.fetchall()

            metric_ids = [row[0] for row in rows]
            return metric_ids

    except Exception as e:
        print(f'Ошибка получения metric_owners: {e}')
        raise

def metric_owners_get_all_owners(metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT 
                    user_id
                FROM Metric_Owners
                WHERE metric_id = ?
                ''',
                (metric_id,)
            )

            rows = result.fetchall()
            user_ids = [row[0] for row in rows]

            return user_ids

    except Exception as e:
        print(f'Ошибка получения metric_owners: {e}')
        raise

def metric_owners_delete_pair(user_id: int, metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Metric_Owners 
                WHERE user_id = ? AND metric_id = ?
                ''',
                (user_id, metric_id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка удаления metric_owners: {e}')
        raise

def metric_owners_get_pair(user_id: int, metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT 
                    *
                FROM Metric_Owners
                WHERE user_id = ? AND metric_id = ?
                ''',
                (user_id, metric_id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка получения metric_owners: {e}')
        raise

def __get_all():
    with get_connection() as conn:
        cursor = conn.cursor()

        res = cursor.execute(
            '''
            SELECT * FROM Metric_Owners
            '''
        )

        column_names = [dsc[0] for dsc in res.description]
        rows = res.fetchall()

        print(column_names)
        for row in rows:
            print(rows)