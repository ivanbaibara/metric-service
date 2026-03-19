from flask import jsonify, request
from functools import wraps

def validate_json(scheme: dict):
    def decorator(func):
        @wraps(func)
        def wrapper():
            try:
                data = request.json

                for field, expected_type in scheme.items():
                    if field not in data:
                        return jsonify({'error': f'Missing: {field} field'}), 400

                    if expected_type is int and not data[field].isdigit():
                        return jsonify({'error': f'Field {field} not a int'}), 400


                # Если все прошло, возвращаем результат обычной функции
                return func()
            except Exception as e:
                print(f'validate json: {e}')
                return jsonify({'error': 'whatever'}), 400

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

                    if expected_type is int and not data[field].isdigit():
                        return jsonify({'error': f'Field {field} not a int'}), 400


                # Если все прошло, возвращаем результат обычной функции
                return func()
            except Exception as e:
                print(f'validate args: {e}')
                return jsonify({'error': 'whatever'}), 400

        return wrapper
    return decorator

def validate_none(func):
    @wraps(func)
    def wrapper():
        try:
            return func()

        except Exception as e:
            return jsonify({'error': 'whatever'})

    return wrapper