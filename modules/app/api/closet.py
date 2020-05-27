import os
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app import app, mongo, jwt
from app.controllers.user import find_user_by_email
from app.controllers.closet import add_item_to_closet, remove_item_from_closet, find_closet_by_id
from app.controllers.clothingitem import find_clothinglist_by_ids
from app.services.formatservice import convert_to_ObjectId
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/closet/<id>', methods=['GET'])
def fetch_closet(id):
    formatted_id = convert_to_ObjectId(id)
    try:
        closet = find_closet_by_id(formatted_id)
        item_list = closet['clothing_items']
        formatted_item_list = map(convert_to_ObjectId, item_list)
        clothingitem_list = find_clothinglist_by_ids(formatted_item_list)
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        return jsonify({'ok': True, 'data': clothingitem_list}), 200


@app.route('/closet/<id>/items', methods=['GET'])
def fetch_closet_item_list(id):
    formatted_id = convert_to_ObjectId(id)
    try:
        closet = find_closet_by_id(formatted_id)
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        item_list = closet['clothing_items']
        return jsonify({'ok': True, 'data': item_list}), 200

@app.route('/closet/item', methods=['POST'])
@jwt_required
def add_to_closet():
    data = request.get_json()
    user_info = get_jwt_identity()
    user = find_user_by_email(user_info['email'])
    user_id = user['_id']
    if user:
        closet_id = user['closet']
        item_id = data['item_id']
        formatted_item_id = convert_to_ObjectId(item_id)
        try:
            add_item_to_closet(closet_id, formatted_item_id)
        except LookupError as err:
            return jsonify({'ok': False, 'message': str(err)}), 404
        except:
            return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
        else:
            LOG.info('Added item {} to closet {} for user {}'.format(item_id, closet_id, user_id))
            return jsonify({'ok': True, 'data': {}}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad user info: {}'.format(user_info['email'])}), 400

@app.route('/closet/item/remove', methods=['POST'])
@jwt_required
def remove_from_closet():
    data = request.get_json()
    user_info = get_jwt_identity()
    user = find_user_by_email(user_info['email'])
    user_id = user['_id']
    if user:
        closet_id = user['closet']
        item_id = data['item_id']
        formatted_item_id = convert_to_ObjectId(item_id)
        try:
            remove_item_from_closet(closet_id, formatted_item_id)
        except LookupError as err:
            return jsonify({'ok': False, 'message': str(err)}), 404
        except:
            return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
        else:
            LOG.info('Removed item {} from closet {} for user {}'.format(item_id, closet_id, user_id))
            return jsonify({'ok': True, 'data': {}}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad user info: {}'.format(user_info['email'])}), 400
