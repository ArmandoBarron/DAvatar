import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    """
    to handle elements ObjectId() into 
    <class 'pymongo.cursor.Cursor'>
    allows to print _id elements like str
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)