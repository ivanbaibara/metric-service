from flask import jsonify, request
from functools import wraps
from datetime import datetime

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_sqlite_timestamp(s: str):
    try:
        datetime.fromisoformat(s)
        return True
    except ValueError:
        return False

def validate_json(scheme: dict):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                data = request.json

                for field, expected_type in scheme.items():
                    if field not in data:
                        return jsonify({'error': f'Missing: {field} field'}), 400

                    if expected_type is int and not is_int(data[field]):
                        return jsonify({'error': f'Field {field} not a int'}), 400

                    if expected_type is float and not is_float(data[field]):
                        return jsonify({'error': f'Field {field} not a float'}), 400


                # Если все прошло, возвращаем результат обычной функции
                return func()
            except Exception as e:
                print(f'validate json: {e}')
                return jsonify({'error': 'Bad request'}), 400

        return wrapper
    return decorator

def validate_args(scheme: dict):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                if scheme is None:
                    return func()

                data = request.args

                for field, expected_type in scheme.items():
                    if field not in data:
                        return jsonify({'error': f'Missing: {field} field'}), 400

                    if expected_type is int and not is_int(data[field]):
                        return jsonify({'error': f'Field {field} not a int'}), 400

                    if expected_type is float and not is_float(data[field]):
                        return jsonify({'error': f'Field {field} not a float'}), 400

                # Если все прошло, возвращаем результат обычной функции
                return func()
            except Exception as e:
                print(f'validate args: {e}')
                return jsonify({'error': 'Bad request'}), 400

        return wrapper
    return decorator

def validate_none(func):
    @wraps(func)
    def wrapper():
        try:
            return func()

        except Exception as e:
            return jsonify({'error': 'Bad request'})

    return wrapper