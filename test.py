import json
import base64
from unittest import TestCase
from main import app
import config
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


app.testing = True
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class test_integrations_user(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_negative_auth(self):
        expected = 'Unauthorized Access'
        response = self.app.get('/user/1',
                                content_type='application/json')
        actual = response.get_data().decode()
        self.assertEqual(
            actual,
            expected
        )

    def test_get_postivie_auth(self):
        expected = {'Id': 1, 'Username': '4', 'Password': '4', 'uri': 'http://localhost/user/1'}
        base64string = base64.encodebytes(('%s:%s' % (expected['Username'], expected['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.get('/user/1',
                                headers=headers,
                                content_type='application/json')
        actual = json.loads(response.get_data().decode())
        self.assertDictEqual(
            actual,
            expected
        )

    def test_put_postivie_auth(self):
        input = {'Id': 1, 'Username': '4', 'Password': '4'}
        expected = {'Id': 1, 'Password': '44', 'Username': '44', 'uri': 'http://localhost/user/1'}
        base64string = base64.encodebytes(('%s:%s' % (input['Username'], input['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.put('/user/1',
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(expected))
        actual = json.loads(response.get_data().decode())
        self.assertDictEqual(
            actual,
            expected
        )


    def test_post_positive_input(self):
        input = {'Username': 'alex', 'Password': 'alex'}
        base64string = base64.encodebytes(('%s:%s' % (input['Username'], input['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.post('/user',
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(input))
        actual = json.loads(response.get_data().decode())
        self.assertTrue('Id' in actual)
