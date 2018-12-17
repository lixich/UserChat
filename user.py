#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from model import user_class, user_set, create_record, update_record

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)

# crud

def create_record(_request, _record):
    # _record is empty, only Ids
    try:
        for _field in user_class.keys():
            if _field not in _record.keys():
                _record[_field] = request.json.get(_field, user_class[_field]())
    except:
        return False
    return True

def update_record(_request, _record):
    for _field in user_class.keys():
        if _field in request.json:
            _record[_field] = request.json[_field]


# security

def make_public_user(user):
    new_user = {}
    for field in user:
        new_user[field] = user[field]
        if field == 'Id':
            new_user['uri'] = url_for('.get_user', user_id = user['Id'], _external = True)
    return new_user

def get_user_id(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Id']

def get_current_user():
    users = [user for user in user_set if user['Username'] == auth.username()]
    if len(users) == 0:
        return None
    return users[0]

@auth.get_password
def get_password(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Password']

# all

@app_user.route('/', methods = ['GET'])
@auth.login_required
def login_required():
    if auth.username():
        users = [user for user in user_set if user['Username'] == auth.username()]
        return jsonify(make_public_user(users[0])), 201
    else:
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app_user.route('/', methods = ['POST'])
def create_user():
    if not request.json:
        abort(400)
    user = { 'Id': user_set[-1]['Id'] + 1 if len(user_set) else 1 }
    if not create_record(request, user):
        abort(400)
    user_set.append(user)
    return jsonify(make_public_user(user)), 201

# by id

@app_user.route('/<int:user_id>', methods = ['GET'])
@auth.login_required
def get_user(user_id):
    users = [user for user in user_set if user['Id'] == user_id]
    current_user = get_current_user()
    if len(users) == 0 or get_current_user()['Id'] != user_id:
        abort(404)
    return jsonify(make_public_user(users[0]))

@app_user.route('/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_dose(user_id):
    users = [dose for dose in user_set if dose['Id'] == user_id]
    if len(users) == 0 or not request.json:
        abort(404)
    user = users[0]
    update_record(request, user)
    return jsonify( make_public_user(user))

@app_user.route('/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    users = [user for user in user_set if user['Id'] == user_id]
    if len(users) == 0:
        abort(404)
    user_set.remove(users[0])
    return jsonify({'Result': True})
