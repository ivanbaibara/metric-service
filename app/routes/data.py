from flask import Blueprint, jsonify
from app.utils.auth import check_auth


data_bp = Blueprint('data', __name__)

@data_bp.route('/api/data', methods=['GET'])
@check_auth(level_required=0)
def get_data():
    return jsonify({'msg': 'you cool'}), 200
