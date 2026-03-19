from flask import Blueprint, request, session, jsonify
from app.utils.tools import validate_json, validate_args, validate_none
from app.utils.auth import check_auth
from app.database.users_db import *
from app.database.token_db import *


users_bp = Blueprint('users', __name__)


USER_ADD_SCHEME = {
    'role': int,
    'login': str,
    'password': str
}

USER_DELETE_SCHEME = {
    'id': int
}

USER_GET_SCHEME_URL = {
    'id': int
}

USER_UPDATE_SCHEME = {
    'password': str
}


@users_bp.route('/api/users', methods=['POST'])
@check_auth(level_required=0)
@validate_json(scheme=USER_ADD_SCHEME)
def user_add():
    data = request.json

    role = int(data['role'])
    login = data['login']
    password = data['password']

    if role not in [0, 1, 2]:
        return jsonify({'error': 'Invalid role value'}), 400

    if not (8 <= len(login) <= 16):
        return jsonify({'error': 'Invalid login length'}), 400

    if not (8 <= len(password) <= 16):
        return jsonify({'error': 'Invalid password length'}), 400

    user = User()
    user.role = role
    user.login = login
    user.password = password

    user_id = users_add(user)
    return jsonify({'added_id': user_id}), 200


@users_bp.route('/api/users', methods=['GET'])
@check_auth(level_required=0)
@validate_args(scheme=USER_GET_SCHEME_URL)
def user_get():
    user_id = request.args['id']

    user = users_get_id(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    return jsonify(user.to_dict()), 200


@users_bp.route('/api/users/all', methods=['GET'])
@check_auth(level_required=0)
@validate_args(scheme=None)
def user_get_all():
    users = users_get_all()
    users_list = [user.to_dict() for user in users]

    return jsonify(users_list), 200


@users_bp.route('/api/users', methods=['DELETE'])
@check_auth(level_required=0)
@validate_json(scheme=USER_DELETE_SCHEME)
def user_delete():
    data = request.json

    user_id = data['id']
    count = users_delete(user_id)

    return jsonify({'deleted': count})


@users_bp.route('/api/users', methods=['PATCH'])
@check_auth(level_required=2)
@validate_json(scheme=USER_UPDATE_SCHEME)
def user_update():
    user_id = session['user_id']
    data = request.json

    password = data['password']

    user = User()
    user.id = user_id
    user.password =password

    # Обновляем и удаляем все старые токены
    count = users_update(user)
    tokens_delete_all_keys(user_id)
    return jsonify({'updated': count}), 200


@users_bp.route('/api/users/self', methods=['GET'])
@check_auth(level_required=2)
@validate_args(scheme=None)
def user_self_get():
    user_id = session['user_id']

    user = users_get_id(user_id)
    return jsonify({
        'id': user.id,
        'role': user.role,
        'login': user.login
    })


