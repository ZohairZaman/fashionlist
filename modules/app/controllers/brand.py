import os
from app import app, mongo
import logger
from app.models.brand import Brand

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

def get_brand_list():
    try:
        brand_list = mongo.db.brand.find()
    except:
        error_message = 'Error occured in the fetch for brands'
        LOG.error(error_message)
        raise LookupError(error_message)
    else:
        formatted_list = []
        for brand in brand_list:
            formatted_brand = Brand.fromdict(brand)
            formatted_list.append(formatted_brand)
        return formatted_list
