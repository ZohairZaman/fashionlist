import os
from app import app, mongo
from app.controllers.clothingitem import find_clothingitem_by_id
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

def create_wishlist(user_id):
    clothing_items = []
    wishlist_entry = {
        "clothing_items": clothing_items,
        "user_id": user_id
    }
    wishlist_id = mongo.db.wishlist.insert_one(wishlist_entry).inserted_id
    LOG.info('Created wish list for user: {}'.format(user_id))
    return wishlist_id

def find_wishlist_by_id(wishlist_id):
    try:
        item = mongo.db.wishlist.find_one({"_id": wishlist_id})
    except:
        error_message = 'Error occured in the fetch for wishlist {}'.format(wishlist_id)
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        if item is None:
            not_found_message = 'Could not found any wishlist with id {}'.format(wishlist_id)
            LOG.info(not_found_message)
            raise LookupError(not_found_message)
        else:
            return item

def add_item_to_wishlist(wishlist_id, item_id):
    try:
        clothing_item = find_clothingitem_by_id(item_id)
        wishlist = find_wishlist_by_id(wishlist_id)
    except LookupError as err:
        raise
    else:
        mongo.db.wishlist.find_one_and_update({"_id": wishlist_id},
                            {"$push": {"clothing_items": item_id}})

def remove_item_from_wishlist(wishlist_id, item_id):
    try:
        clothing_item = find_clothingitem_by_id(item_id)
        wishlist = find_wishlist_by_id(wishlist_id)
    except LookupError as err:
        raise
    else:
        mongo.db.wishlist.find_one_and_update({"_id": wishlist_id},
                            {"$pull": {"clothing_items": item_id}})
