"""ECS pretty print for json objects"""
import datetime
import json
from json import JSONEncoder
from typing import Dict


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    """DateTime Encoder for Json."""

    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def get_pretty_json_str(obj, indent=2):
    """Print the json object."""
    return json.dumps(obj, indent=indent, cls=DateTimeEncoder)
