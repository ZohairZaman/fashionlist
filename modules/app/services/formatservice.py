from bson.objectid import ObjectId
from bson.json_util import dumps

def convert_to_ObjectId(id):
    return ObjectId(id)

def convert_ObjectId_to_string(id):
    return str(id)

def convert_to_JSON(obj):
    return dumps(obj)
