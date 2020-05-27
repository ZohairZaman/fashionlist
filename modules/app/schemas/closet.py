from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

closet_schema = {
    "type": "object",
    "properties": {
        "clothing_items": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },
        "user_id": {
            "type": "string"
        }
    },
    "required": ["clothing_items", "user_id"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, closet_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
