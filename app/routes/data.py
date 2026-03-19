from flask import Blueprint, jsonify
from app.utils.auth import check_auth
from app.utils.tools import validate_json, validate_args
from app.database.data_flt_db import *

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/data', methods=['GET'])
@check_auth(level_required=0)
def get_data():
    return jsonify({'msg': 'you cool'}), 200
