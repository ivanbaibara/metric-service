from flask import Blueprint, request, session, jsonify
from app.database.token_db import tokens_add_key, tokens_delete_key
from app.database.users_db import users_get_login, users_check_password
from app.utils.auth import check_auth


login_bp = Blueprint('login', __name__)

# json request format: {'login': <login>, 'password': <password>}
@login_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('login')
    password = data.get('password')

    user = users_get_login(username)

    if user is None:
        return jsonify({'msg': 'This user not exists'}), 401

    # Проверяем пароль
    if users_check_password(user['id'], password):
        token = tokens_add_key(user['id'])

        session['user_id'] = user['id']
        session['token'] = token

        return jsonify({'msg': 'Logged in'}), 200

    return jsonify({'msg': 'Invalid credentials'}), 401


@login_bp.route('/api/logout', methods=['POST'])
@check_auth(level_required=3)
def logout():
    user_id = session['user_id']
    token = session['token']
    tokens_delete_key(user_id, token)
    session.clear()

    return jsonify({'msg': 'logged out'}), 200
