from flask import session, jsonify
from app.database.token_db import tokens_check_key
from app.database.users_db import users_get_id
from functools import wraps

def check_auth(level_required):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id', -1)
            token = session.get('token', '')

            access_flag = False
            level_flag = False
            if user_id != -1 and token != '':
                # Проверяем доступ
                access_flag = tokens_check_key(user_id, token)

                # Проверяем уровень доступа
                user = users_get_id(user_id)
                level_flag = int(user['role']) <= level_required

            if access_flag and level_flag:
                return func()
            elif access_flag and not level_flag:
                return jsonify({'msg': 'Denied access'}), 401
            else:
                return jsonify({'msg': 'Not authorized'}), 401

        return wrapper
    return decorator