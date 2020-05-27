import os
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
from app.schemas.user import validate_user
from app.controllers.closet import create_closet
from app.controllers.user import find_user_by_id
from app.controllers.wishlist import create_wishlist
from app.services.formatservice import convert_to_ObjectId, convert_to_JSON
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

@app.route('/user/<user_id>', methods=['GET'])
@jwt_required
def fetch_user(user_id):
    formatted_user_id = convert_to_ObjectId(user_id)
    try:
        user = find_user_by_id(formatted_user_id)
        response = {
            'closet_id': user.closet_id,
            'email': user.email,
            'id': user.id,
            'name': user.name,
            'wishlist_id': user.wishlist_id
        }
    except LookupError as err:
        return jsonify({'ok': False, 'message': str(err)}), 404
    except:
        return jsonify({'ok': False, 'message': 'Unexpected error'}), 404
    else:
        return jsonify({'ok': True, 'data': response}), 200

@app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.user.find_one(query)
        return jsonify({'ok': True, 'data': data}), 200
    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.user.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.user.update_one(data['query'], {'$set':
                data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@app.route('/register', methods=['POST'])
def register():
    ''' register user endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(
                            data['password'])
        user_id = mongo.db.user.insert_one(data).inserted_id
        closet_id = create_closet(user_id)
        wishlist_id = create_wishlist(user_id)
        mongo.db.user.find_one_and_update({"_id": user_id},
                                 {"$set": {"closet": closet_id, "wishlist": wishlist_id}})
        LOG.info('Registered user: {}'.format(user_id))
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/auth', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.user.find_one({'email': data['email']})
        is_valid_user = user is not None
        is_valid_password = is_valid_user and flask_bcrypt.check_password_hash(user['password'], data['password'])
        if is_valid_user:
            if is_valid_password:
                del user['password']
                access_token = create_access_token(identity=data)
                refresh_token = create_refresh_token(identity=data)
                user['token'] = access_token
                user['refresh'] = refresh_token
                return jsonify({'ok': True, 'data': user}), 200
            else:
                return jsonify({'ok': False, 'message': 'Invalid password'}), 401
        else:
            return jsonify({'ok': False, 'message': 'Invalid email'}), 401

    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
            'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200
