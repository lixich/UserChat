#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)
db = SQLAlchemy()


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

# security

def make_public_user(user):
    new_user = {}
    new_user['uri'] = url_for('.get_user', user_id = user.Id, _external = True)
    new_user['Id'] = user.Id
    new_user['Username'] = user.Username
    new_user['Password'] = user.Password
    return new_user

def get_user_id(username):
    user = User.query.filter_by(Username=username).first()
    if not user:
        return None
    return user.Id

def get_current_user():
    user = User.query.filter_by(Username=auth.username()).first()
    if not user:
        return None
    return user

@auth.get_password
def get_password(username):
    user = User.query.filter_by(Username=username).first()
    if not user:
        return None
    return user.Password

# all

@app_user.route('/', methods = ['GET'])
@auth.login_required
def login_required():
    if auth.username():
        user = User.query.filter_by(Username=auth.username()).first()
        return jsonify(make_public_user(user)), 201
    else:
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app_user.route('/', methods = ['POST'])
def create_user():
    if not request.json:
        abort(400)
    user = User(request.json['Username'], request.json['Password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(make_public_user(user))

# by id

@app_user.route('/<int:user_id>', methods = ['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.filter_by(Id=user_id).first()
    current_user = get_current_user()
    if not user or get_current_user().Id != user_id:
        abort(404)
    return jsonify(make_public_user(user))

@app_user.route('/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = User.query.filter_by(Id=user_id).first()
    if not user or not request.json:
        abort(404)
    user.Username = request.json['Username']
    user.Password = request.json['Password']
    db.session.commit()
    return jsonify( make_public_user(user))

@app_user.route('/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = User.query.filter_by(Id=user_id).first()
    #todo remove
    return jsonify({'Result': False})
