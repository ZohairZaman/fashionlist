from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

listing_schema = {
    "type": "object",
    "properties": {
        "clothing_item": {
            "type": "string"
        }
    },
    "required": ["clothing_item"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, listing_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
