from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

brand_schema = {
    "type": "object",
    "properties": {
        "listings": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },
        "name": {
            "type": "string"
        }
    },
    "required": ["name"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, brand_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
