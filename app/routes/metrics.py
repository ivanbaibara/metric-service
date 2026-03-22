from flask import Blueprint, session, jsonify, request
from app.utils.auth import check_auth
from app.database.metric_owners_db import *
from app.database.metrics_db import *
from app.database.users_db import *
from app.database.operations import *
from app.utils.tools import validate_json, validate_args


metrics_bp = Blueprint('metrics', __name__)

METRIC_ADD_SCHEME = {
    'name': str,
    'type': str,
    'duration': int
}

METRIC_DELETE_SCHEME = {
    'id': int
}

METRIC_UPDATE_SCHEME = {
    'id': int,
    'name': str,
    'duration': int
}

METRIC_GET_SCHEME_URL = {
    'id': int
}

METRIC_PERMISSIONS_SCHEME = {
    'id': int,
    'user_login': str
}

METRIC_PERMISSIONS_GET_SCHEME_URL = {
    'id': int
}


@metrics_bp.route('/api/metrics', methods=['POST'])
@check_auth(level_required=1)
@validate_json(scheme=METRIC_ADD_SCHEME)
def metric_add():
    user_id = session['user_id']
    data = request.json

    metric = Metric()
    metric.name = data.get('name')
    metric.type = data.get('type')
    metric.duration = int(data.get('duration'))

    if not (4 <= len(metric.name) <= 32):
        return jsonify({'error': 'Invalid name length'}), 400

    if len(metric.type) != 3:
        return jsonify({'error': 'Invalid type length'}), 400

    if metric.duration <= 0:
        return jsonify({'error': 'Invalid duration value'}), 400

    # Добавление в БД
    metric = transaction_metric_add(user_id, metric)

    return jsonify({'add_id': metric.id}), 200


@metrics_bp.route('/api/metrics', methods=['DELETE'])
@check_auth(level_required=1)
@validate_json(scheme=METRIC_DELETE_SCHEME)
def metric_delete():
    user_id = session['user_id']
    data = request.json

    metric = Metric()
    metric.id = int(data.get('id'))

    # проверяем, если доступ к метрике у пользователя
    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric.id in user_metrics:
        count = metrics_delete(metric)
        return jsonify({'deleted_count': count}), 200

    else:
        return jsonify({'error': 'Denied'}), 400


@metrics_bp.route('/api/metrics', methods=['PATCH'])
@check_auth(level_required=1)
@validate_json(scheme=METRIC_UPDATE_SCHEME)
def metric_update():
    user_id = session['user_id']
    data = request.json

    metric = Metric()
    metric.id = int(data.get('id'))

    # проверяем, есть ли доступ к метрике
    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric.id not in user_metrics:
        return jsonify({'error': 'Denied'})

    if not (4 <= len(data.get('name')) <= 32):
        return jsonify({'error': 'Invalid name length'}), 400

    if int(data.get('duration')) <= 0:
        return jsonify({'error': 'Invalid duration value'}), 400

    metric.name = data.get('name')
    metric.duration = int(data.get('duration'))
    count = metrics_update(metric)

    return jsonify({'updated': count})


@metrics_bp.route('/api/metrics', methods=['GET'])
@check_auth(level_required=2)
@validate_args(scheme=METRIC_GET_SCHEME_URL)
def metric_get():
    user_id = session['user_id']

    metric = Metric()
    metric.id = int(request.args.get('id'))

    # Проверяем, есть ли доступ к метрике
    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric.id in user_metrics:
        metric = metrics_get(metric.id)
        return jsonify(metric.to_dict()), 200

    return jsonify({'error': 'Denied'}), 400


@metrics_bp.route('/api/metrics/all', methods=['GET'])
@check_auth(level_required=2)
@validate_args(scheme=None)
def metric_get_ids():
    user_id = session['user_id']
    user_metrics = metric_owners_get_all_metrics(user_id)
    return jsonify(user_metrics), 200


@metrics_bp.route('/api/metrics/permissions', methods=['POST'])
@check_auth(level_required=1)
@validate_json(scheme=METRIC_PERMISSIONS_SCHEME)
def metric_add_owner():
    user_id = session['user_id']

    # Можем добавлять только наблюдателей (уровень доступа 2)
    metric_id = request.json['id']
    add_user_login = request.json['user_login']

    # Проверяем наличие что первого что второго в таблицах
    metric = metrics_get(metric_id)
    user = users_get_login(add_user_login)

    user_metrics = metric_owners_get_all_metrics(user_id)

    if not metric:
        return jsonify({'error': 'Metric not found'}), 400

    if metric.id not in user_metrics:
        return jsonify({'error': 'Denied access'}), 401

    if not user:
        return jsonify({'error': 'User not found'}), 400

    if user.role != 2:
        return jsonify({'error': 'You cannot add user without spectator role'}), 400

    # Проверка на наличии прав
    permission = metric_owners_get_pair(user.id, metric.id)

    if permission:
        return jsonify({'error': 'User already has permission'}), 400

    count = metric_owners_add(user.id, metric.id)
    return jsonify({'added': count}), 200


@metrics_bp.route('/api/metrics/permissions', methods=['DELETE'])
@check_auth(level_required=1)
@validate_json(scheme=METRIC_PERMISSIONS_SCHEME)
def metric_delete_owner():
    user_id = session['user_id']

    # Нельзя удалить себя
    metric_id = request.json['id']
    delete_user_login = request.json['user_login']

    metric = metrics_get(metric_id)
    user = users_get_login(delete_user_login)

    user_metrics = metric_owners_get_all_metrics(user_id)

    if not metric:
        return jsonify({'error': 'Metric not found'}), 400

    if metric.id not in user_metrics:
        return jsonify({'error': 'Denied access'}), 401

    if not user:
        return jsonify({'error': 'User not found'}), 400

    if metric_owners_get_pair(user_id, metric_id) == 0:
        return jsonify({'error': 'Not permissions found for user'})

    if user.id == user_id:
        return jsonify({'error': 'You cannot delete yourself'}), 400

    count = metric_owners_delete_pair(user.id, metric_id)
    return jsonify({'deleted': count})


@metrics_bp.route('/api/metrics/permissions', methods=['GET'])
@check_auth(level_required=1)
@validate_args(scheme=METRIC_PERMISSIONS_GET_SCHEME_URL)
def metric_get_owner():
    user_id = session['user_id']
    metric_id = int(request.args['id'])

    metric = metrics_get(metric_id)
    user_metrics = metric_owners_get_all_metrics(user_id)

    if not metric:
        return jsonify({'error': 'Not found'}), 400

    if metric_id not in user_metrics:
        return jsonify({'error': 'Denied access'}), 401

    metric_all_owners = metric_owners_get_all_owners(metric_id)
    users_login = []

    for owner_id in metric_all_owners:
        user = users_get_id(owner_id)
        users_login.append(user.login)

    return jsonify(users_login), 200
