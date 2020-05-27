import os
from app import app, mongo
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

def find_clothingitem_by_id(item_id):
    try:
        item = mongo.db.clothingitem.find_one({"_id": item_id})
    except:
        error_message = 'Error occured in the fetch for clothing item {}'.format(item_id)
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        if item is None:
            not_found_message = 'Could not find any clothing item with id {}'.format(item_id)
            LOG.info(not_found_message)
            raise LookupError(not_found_message)
        else:
            return item

def find_clothinglist_by_ids(id_list):
    item_list = []
    for id in id_list:
        try:
            item = find_clothingitem_by_id(id)
            item_list.append(item)
        except LookupError as err:
            pass
        except:
            raise
    if item_list is None:
        not_found_message = 'Could not find any clothing item in this id list'
        LOG.info(not_found_message)
        raise LookupError(not_found_message)
    else:
        return item_list
