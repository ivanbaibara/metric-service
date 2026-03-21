from flask import Blueprint, jsonify, request, session
from app.utils.auth import check_auth
from app.utils.tools import validate_json, validate_args, is_sqlite_timestamp
from app.database.data_flt_db import *
from app.database.metric_owners_db import *


data_bp = Blueprint('data', __name__)

DATA_ADD_SCHEME = {
    'id': int,
    'value': float
}

DATA_GET_SCHEME_URL = {
    'id': int
}

@data_bp.route('/api/data', methods=['POST'])
@check_auth(level_required=1)
@validate_json(scheme=DATA_ADD_SCHEME)
def data_add():
    user_id = session['user_id']

    metric_id = int(request.json['id'])
    value = float(request.json['value'])

    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric_id not in user_metrics:
        return jsonify({'error': 'Denied access'})

    count = data_flt_add(metric_id, value)
    return jsonify({'added': count}), 200


@data_bp.route('/api/data', methods=['GET'])
@check_auth(level_required=2)
@validate_args(scheme=DATA_GET_SCHEME_URL)
def data_get():
    user_id = session['user_id']

    metric_id = int(request.args['id'])

    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric_id not in user_metrics:
        return jsonify({'error': 'Denied access'}), 400

    # check other field:
    after = request.args.get('after')
    until = request.args.get('until')

    if after and not is_sqlite_timestamp(after):
        return jsonify({'error': 'Invalid after timestamp field'}), 400

    if until and not is_sqlite_timestamp(until):
        return jsonify({'error': 'Invalid until timestamp field'}), 400

    if after:
        after = after.replace('_', ' ')

    if until:
        until = until.replace('_', ' ')

    data = data_flt_get_many(metric_id, after, until)

    return jsonify(data), 200


@data_bp.route('/api/data/last', methods=['GET'])
@check_auth(level_required=2)
@validate_args(scheme=DATA_GET_SCHEME_URL)
def data_get_last():
    user_id = session['user_id']

    metric_id = int(request.args['id'])

    user_metrics = metric_owners_get_all_metrics(user_id)

    if metric_id not in user_metrics:
        return jsonify({'error': 'Denied access'}), 400

    data = data_flt_get_last(metric_id)

    return jsonify(data), 200


