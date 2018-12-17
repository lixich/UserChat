from flask import request
from sqlalchemy import inspect

#todo database
message_set = [
    {
        'Id': 1,
        'Text': 'Hello!',
        'Time': '',
        'UserId': 1
    },
    {
        'Id': 2,
        'Text': 'How are you?',
        'Time': '',
        'UserId': 1
    }
]
message_class = {
    'Id': int,
    'Text': str,
    'Time': str,
    'UserId': int
}

#crud
def create_record(_class, _request, _record):
    try:
        for _field in _class.keys():
            if _field not in _record.keys():
                _record[_field] = request.json.get(_field, _class[_field]())
    except:
        return False
    return True

def update_record(_class, _request, _record):
    for _field in _class.keys():
        if _field in request.json:
            _record[_field] = request.json[_field]
