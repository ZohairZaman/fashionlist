import os
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app import app, mongo, jwt
from app.controllers.user import find_user_by_email
from app.controllers.wishlist import add_item_to_wishlist, remove_item_from_wishlist, find_wishlist_by_id
from app.controllers.clothingitem import find_clothinglist_by_ids
from app.services.formatservice import convert_to_ObjectId
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/wishlist/<id>', methods=['GET'])
@jwt_required
def fetch_wishlist(id):
    formatted_id = convert_to_ObjectId(id)
    try:
        wishlist = find_wishlist_by_id(formatted_id)
        item_list = wishlist['clothing_items']
        formatted_item_list = map(convert_to_ObjectId, item_list)
        clothingitem_list = find_clothinglist_by_ids(formatted_item_list)
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        return jsonify({'ok': True, 'data': clothingitem_list}), 200

@app.route('/wishlist/<id>/items', methods=['GET'])
@jwt_required
def fetch_wishlist_item_list(id):
    formatted_id = convert_to_ObjectId(id)
    try:
        wishlist = find_wishlist_by_id(formatted_id)
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        item_list = wishlist['clothing_items']
        return jsonify({'ok': True, 'data': item_list}), 200

@app.route('/wishlist/item', methods=['POST'])
@jwt_required
def add_to_wishlist():
    data = request.get_json()
    user_info = get_jwt_identity()
    user = find_user_by_email(user_info['email'])
    user_id = user['_id']
    if user:
        wishlist_id = user['wishlist']
        item_id = data['item_id']
        formatted_item_id = convert_to_ObjectId(item_id)
        try:
            add_item_to_wishlist(wishlist_id, formatted_item_id)
        except LookupError as err:
            return jsonify({'ok': False, 'message': str(err)}), 404
        except:
            return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
        else:
            LOG.info('Added item {} to wishlist {} for user {}'.format(item_id, wishlist_id, user_id))
            return jsonify({'ok': True, 'data': {}}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad user info: {}'.format(user_info['email'])}), 400

@app.route('/wishlist/item/remove', methods=['POST'])
@jwt_required
def remove_from_wishlist():
    data = request.get_json()
    user_info = get_jwt_identity()
    user = find_user_by_email(user_info['email'])
    user_id = user['_id']
    if user:
        wishlist_id = user['wishlist']
        item_id = data['item_id']
        formatted_item_id = convert_to_ObjectId(item_id)
        try:
            remove_item_from_wishlist(wishlist_id, formatted_item_id)
        except LookupError as err:
            return jsonify({'ok': False, 'message': str(err)}), 404
        except:
            return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
        else:
            LOG.info('Removed item {} from wishlist {} for user {}'.format(item_id, wishlist_id, user_id))
            return jsonify({'ok': True, 'data': {}}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad user info: {}'.format(user_info['email'])}), 400
