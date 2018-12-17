from flask import request
'''
from main import db
from sqlalchemy import inspect

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class User(db.Model):
    __tablename__ = 'User'
    Id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    Username = db.Column(db.String, nullable=False, unique=True)
    Password = db.Column(db.String, nullable=False)
    def __repr__(self):
        return "<Username: {}>".format(self.Username)
    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password
'''

#todo database
#user_set = list(map(object_as_dict, db.session.query(User)))
user_set = [
    {
        'Id': 1,
        'Username': '1',
        'Password': '1',
    }
]
user_class = {
    'Id': int,
    'Username': str,
    'Password': str
}

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
