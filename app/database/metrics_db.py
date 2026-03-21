import sqlite3

from config import *
'''
Metrics (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    type CHAR(3) NOT NULL,
    duration INTEGER NOT NULL 
)
'''

class Metric:
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.duration = None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'duration': self.duration
        }

def get_connection():
    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

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


# Not used
def metrics_add(metric: Metric):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                INSERT INTO Metrics (name, type, duration)
                VALUES (?, ?, ?)
                ''',
                (metric.name, metric.type, metric.duration)
            )

            return result.lastrowid

    except Exception as e:
        print(f'Ошибка добавления metric: {e}')
        raise

def metrics_get(metric_id: int) -> Metric | None:
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
                (metric_id,)
            )

            row = result.fetchone()
            if row:
                metric = Metric()
                metric.id = row[0]
                metric.name = row[1]
                metric.type = row[2]
                metric.duration = row[3]

                return metric

    except Exception as e:
        print(f'Ошибка получения metric: {e}')
        raise

def metrics_update(metric: Metric):
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
                (metric.name, metric.duration, metric.id)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка обновления metric: {e}')
        raise

def metrics_delete(metric: Metric):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            result = cursor.execute(
                '''
                DELETE FROM Metrics WHERE id = ?
                ''',
                (metric.id,)
            )

            return result.rowcount

    except Exception as e:
        print(f'Ошибка удаления metric: {e}')
        raise

def __get_all():
    with get_connection() as conn:
        cursor = conn.cursor()

        res = cursor.execute(
            '''
            SELECT * FROM Metrics
            '''
        )

        column_names = [dsc[0] for dsc in res.description]
        rows = res.fetchall()

        print(column_names)
        for row in rows:
            print(row)

