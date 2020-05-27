import os
from app import app, mongo
from flask import request, jsonify
from app.schemas.clothingitem import validate_user
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/item', methods=['GET', 'POST'])
def item():
    if request.method == 'GET':
        query = request.args
        LOG.info('request args: {}'.format(query))
        data = mongo.db.clothingitem.find_one(query)
        return jsonify({'ok': True, 'data': data}), 200
    if request.method == 'POST':
        data = validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            mongo.db.clothingitem.insert_one(data)
            LOG.info('Created clothing item with data: {}'.format(data))
            return jsonify({'ok': True, 'message': 'Clothing item created successfully!'}), 200
        else:
            LOG.info('Could not validate'.format(data['message']))
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/items/', defaults={'page': 1})
@app.route('/items/page=<int:page>')
def get_item(page):
    query = request.args
    PER_PAGE = 40
    LOG.info('request args: {}'.format(query))
    data = list(mongo.db.clothingitem.find(query))
    paginated_data = get_items_for_page(data, page, PER_PAGE)
    return jsonify({'ok': True, 'data': paginated_data}), 200

def get_items_for_page(data, page, per_page):
    start_page_index = page * per_page
    data_size = len(data)
    start_index = max(start_page_index, 0)
    end_index = min(start_page_index + per_page, data_size)
    return data[start_index:end_index]
