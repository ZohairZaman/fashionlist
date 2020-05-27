import os
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app import app, mongo, jwt
from app.controllers.user import find_user_by_email
from app.controllers.brand import get_brand_list
from app.services.formatservice import convert_to_ObjectId
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/brands/preview', methods=['GET'])
def get_brands():
    try:
        brand_list = get_brand_list()
        name_list = []
        for brand in brand_list:
            name_list.append(brand.name)
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        return jsonify({'ok': True, 'data': name_list}), 200
