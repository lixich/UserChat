#!flask/bin/python
import config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

def register_blueprints():
    from user import app_user
    from message import app_message
    app.register_blueprint(app_user, url_prefix='/user')
    app.register_blueprint(app_message, url_prefix='/message')

register_blueprints()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host=config.HOST,debug = True, threaded=True)
