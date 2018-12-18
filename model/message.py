from flask import Blueprint, jsonify, abort, request, make_response
from model.user import auth, get_user_id
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app_message = Blueprint('message', __name__)
db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'Message'
    Id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    Text = db.Column(db.String, nullable=False)
    Time = db.Column(db.String, nullable=False)
    UserId = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"<{self.UserId}: {self.Text}>"
    def __init__(self, Text, UserId):
        self.Text = Text
        self.Time = str(datetime.now())
        self.UserId = UserId

# todo refactoring
def make_dict_message(message):
    dict_message = {}
    dict_message['Id'] = message.Id
    dict_message['Text'] = message.Text
    dict_message['Time'] = message.Time
    dict_message['UserId'] = message.UserId
    return dict_message

# all
@app_message.route('/', methods = ['GET'])
@auth.login_required
def get_message_set():
    if auth.username():
        message_set = Message.query.all()
        # todo refactoring
        result = []
        for mes in message_set:
            mes_dict = mes.__dict__
            mes_dict.pop('_sa_instance_state')
            result.append(mes_dict)
        return json.dumps(result), 201
    else:
        return make_response(jsonify({ 'error': 'Not found' } ), 404)

@app_message.route('/', methods=['POST'])
@auth.login_required
def create_message():
    if not request.json:
        abort(400)
    message = Message(request.json['Text'], get_user_id(auth.username()))
    db.session.add(message)
    db.session.commit()
    return jsonify(make_dict_message(message)), 201
