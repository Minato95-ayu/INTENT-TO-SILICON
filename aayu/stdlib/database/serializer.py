import json

class Serializer:
    @staticmethod
    def to_json(row):
        return json.dumps(row)
