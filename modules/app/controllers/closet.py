import os
from app import app, mongo
from app.controllers.clothingitem import find_clothingitem_by_id
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

def create_closet(user_id):
    clothing_items = []
    closet_entry = {
        "clothing_items": clothing_items,
        "user_id": user_id
    }
    closet_id = mongo.db.closet.insert_one(closet_entry).inserted_id
    LOG.info('Created closet {} for user {}'.format(user_id))
    return closet_id

def find_closet_by_id(closet_id):
    try:
        item = mongo.db.closet.find_one({"_id": closet_id})
    except:
        error_message = 'Error occured in the fetch for closet {}'.format(closet_id)
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        if item is None:
            not_found_message = 'Could not found any closet with id {}'.format(closet_id)
            LOG.info(not_found_message)
            raise LookupError(not_found_message)
        else:
            return item

def add_item_to_closet(closet_id, item_id):
    try:
        clothing_item = find_clothingitem_by_id(item_id)
        closet = find_closet_by_id(closet_id)
        return mongo.db.closet.find_one_and_update({"_id": closet_id},
                            {"$push": {"clothing_items": item_id}})
    except:
        raise

def remove_item_from_closet(closet_id, item_id):
    try:
        clothing_item = find_clothingitem_by_id(item_id)
        closet = find_closet_by_id(closet_id)
        return mongo.db.closet.find_one_and_update({"_id": closet_id},
                            {"$pull": {"clothing_items": item_id}})
    except:
        raise
