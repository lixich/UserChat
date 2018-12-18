#!flask/bin/python
import config
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


def register_blueprints():
    from model.user import app_user, db as db_user
    from model.message import app_message
    app.register_blueprint(app_user, url_prefix='/user')
    app.register_blueprint(app_message, url_prefix='/message')
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db_user.init_app(app)
    with app.app_context():
        db_user.create_all()

register_blueprints()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host=config.HOST,debug = True, threaded=True)
