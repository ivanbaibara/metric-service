import sqlite3
import os

from config import *


'''
Data_Flt (
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_id INTEGER NOT NULL REFERENCES Metrics(id) ON DELETE CASCADE,
    value REAL NOT NULL,
    PRIMARY KEY (recorded_at, metric_id)
)
'''

def get_connection():
    conn = sqlite3.connect(DB_FULL_PATH)
    #conn.execute("PRAGMA foreign_keys = ON")
    return conn

def data_flt_create():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Data_Flt (
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metric_id INTEGER NOT NULL REFERENCES Metrics(id) ON DELETE CASCADE,
                    value REAL NOT NULL,
                    PRIMARY KEY (recorded_at, metric_id)
                )
                '''
            )

    except Exception as e:
        print(f'Ошибка создания data_flt: {e}')
        raise

def data_flt_add(metric_id: int, value: float):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                INSERT INTO Data_Flt (metric_id, value)
                VALUES (?, ?)
                ''',
                (metric_id, value)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка добавления data_flt: {e}')
        raise

def data_flt_get_last(metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT 
                    recorded_at,
                    metric_id,
                    value
                FROM Data_Flt
                WHERE metric_id = ?
                ORDER BY recorded_at DESC
                LIMIT 1
                ''',
                (metric_id,)
            )

            row = result.fetchone()

            if row:
                return {
                    'recorded_at': row[0],
                    'metric_id': row[1],
                    'value': row[2]
                }

    except Exception as e:
        print(f'Ошибка получения data_flt: {e}')
        raise

def data_flt_get_many(metric_id: int, after: str, until: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                SELECT 
                    recorded_at,
                    value
                FROM Data_Flt
                WHERE metric_id = ? AND
                recorded_at >= ? AND 
                recorded_at <= ?
                ''',
                (metric_id, after, until)
            )

            rows = result.fetchall()

            data = [ [row[0], row[1]] for row in rows ]
            return data

    except Exception as e:
        print(f'Ошибка получения data_flt: {e}')
        raise

def data_flt_delete_before(metric_id: int, before: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Data_Flt
                WHERE metric_id = ? AND
                recorded_at < ?
                ''',
                (metric_id, before)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка удаления data_flt: {e}')
        raise

def data_flt_delete_all(metric_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Data_Flt WHERE metric_id = ?
                ''',
                (metric_id,)
            )

    except Exception as e:
        print(f'Ошибка удаления data_flt: {e}')
        raise

