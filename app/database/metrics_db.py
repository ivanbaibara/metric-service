import sqlite3
import os

from db_config import DATA_PATH, DB_NAME

DB_FULL_PATH = os.path.join(DATA_PATH, DB_NAME)

'''
Metrics (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    type CHAR(3) NOT NULL,
    duration INTEGER NOT NULL 
)
'''

def get_connection():
    return sqlite3.connect(DB_FULL_PATH)

def metrics_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Metrics (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    type CHAR(3) NOT NULL,
                    duration INTEGER NOT NULL 
                )
                '''
            )

    except Exception as e:
        print(f'Ошибка создания metrics: {e}')
        raise

def metrics_add(add: dict):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                INSERT INTO Metrics (name, type, duration)
                VALUES (?, ?, ?)
                ''',
                (add['name'], add['type'], add['duration'])
            )

            return result.lastrowid

    except Exception as e:
        print(f'Ошибка добавления metric: {e}')
        raise

def metrics_get(metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT 
                    id, name, type, duration
                FROM Metrics
                WHERE id = ?
                ''',
                (metric_id, )
            )

            row = result.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'duration': row[3]
                }

    except Exception as e:
        print(f'Ошибка получения metric: {e}')
        raise

def metrics_update(metric_id: int, update: dict):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                UPDATE Metrics
                SET 
                    name = COALESCE(?, name),
                    duration = COALESCE(?, duration)
                WHERE id = ?
                ''',
                (update['name'], update['duration'], metric_id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка обновления metric: {e}')
        raise

def metrics_delete(metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Metrics WHERE id = ?
                ''',
                (metric_id,)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка удаления metric: {e}')
        raise
