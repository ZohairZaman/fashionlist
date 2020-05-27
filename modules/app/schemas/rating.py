from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

rating_schema = {
    "type": "object",
    "properties": {
        "account": {
            "type": "string",
        },
        "rating": {
            "type": "integer"
        },
        "clothing_item": {
            "type": "string"
        }
    },
    "required": ["account", "rating", "clothing_item"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, rating_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
