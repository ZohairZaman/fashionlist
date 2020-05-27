from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

clothingitem_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "sizing": {
            "type": "string"
        },
        "category": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        },
        "brand": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        },
        "rating": {
            "type": "number"
        },
        "number_of_ratings": {
            "type": "number"
        },
        "retail_price": {
            "type": "number"
        },
        "market_price": {
            "type": "number"
        },
        "description": {
            "type": "string"
        },
        "season": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "release_date": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "listings": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "images": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        },
        "colorway": {
            "type": "string"
        },
        "associated_colors": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "style_id": {
            "type": "string"
        },
        "closet_count": {
            "type": "number"
        }
    },
    "required": ["name", "brand", "category", "images"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, clothingitem_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
