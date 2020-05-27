''' controller and routes for user '''
import os
from app import mongo
from app.models.user import User
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

def find_user_by_email(email):
    try:
        user = mongo.db.user.find_one({"email": email})
    except:
        error_message = 'Error occured in the fetch for user {}'.format(email)
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        if user is None:
            not_found_message = 'Could not find any user with email {}'.format(email)
            LOG.info(not_found_message)
            raise LookupError(not_found_message)
        else:

            return user

def find_user_by_id(user_id):
    try:
        user = mongo.db.user.find_one({"_id": user_id})
    except:
        error_message = 'Error occured in the fetch for user {}'.format(user_id)
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        if user is None:
            not_found_message = 'Could not find any user with id {}'.format(user_id)
            LOG.info(not_found_message)
            raise LookupError(not_found_message)
        else:
            formatted_user = User(
                id = str(user['_id']),
                email = user['email'],
                closet_id = str(user['closet']),
                wishlist_id = str(user['wishlist']),
            )
            return formatted_user
