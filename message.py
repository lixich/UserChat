from flask import Blueprint, jsonify, abort, request, url_for
from user import auth, get_user_id
from datetime import datetime
from model import message_class, message_set, create_record

app_message = Blueprint('message', __name__)

# all
@app_message.route('/', methods = ['GET'])
@auth.login_required
def get_message_set():
    return jsonify(message_set)

@app_message.route('/', methods=['POST'])
@auth.login_required
def create_message():
    if not request.json:
        abort(400)
    message = { 'Id': message_set[-1]['Id'] + 1 if len(message_set) else 1 }
    message['UserId'] = get_user_id(auth.username())
    if not create_record(message_class, request, message):
        abort(400)
    message_set.append(message)
    return jsonify(message), 201

