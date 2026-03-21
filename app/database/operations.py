import sqlite3

from app.database.metrics_db import Metric
from config import DB_FULL_PATH


def get_connection():
    return sqlite3.connect(DB_FULL_PATH, isolation_level=None)


def transaction_metric_add(user_id: int, metric: Metric):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('BEGIN TRANSACTION')
            cursor.execute(
                '''
                INSERT INTO Metrics (name, type, duration)
                VALUES (?, ?, ?)
                ''',
                (metric.name, metric.type, metric.duration)
            )

            metric.id = cursor.lastrowid

            cursor.execute(
                '''
                INSERT INTO Metric_Owners (user_id, metric_id)
                VALUES (?, ?)
                ''',
                (user_id, metric.id)
            )
            conn.commit()

            return metric

    except Exception as e:
        print(f'Ошибка транзакции metric_add: {e}')
        raise
