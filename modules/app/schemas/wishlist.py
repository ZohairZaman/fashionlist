from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

wishlist_schema = {
    "type": "object",
    "properties": {
        "clothing_items": {
            "type": "array",
            "items": {
                "type": "string"
            },
        }
    },
    "required": ["clothing_items"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, wishlist_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
