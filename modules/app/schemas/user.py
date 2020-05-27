from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
import os
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "username": {
            "type": "string"
        },
        "closet": {
            "type": "string"
        },
        "wishlist": {
            "type": "string"
        },
        "ratings": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "phone": {
            "type": "string"
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        LOG.error("Validation error occured on user: {}".format(e))
        return {'ok': False, 'message': e}
    except SchemaError as e:
        LOG.error("Schema error occured on user: {}".format(e))
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
