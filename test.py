import json
import base64
from unittest import TestCase
from main import app
import config
from flask_sqlalchemy import SQLAlchemy

app.testing = True
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# arrane test db
db.engine.execute('''DELETE FROM User''')
db.engine.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="User"''')
db.engine.execute('''
INSERT INTO User (Username, Password)  
VALUES ("1", "1"),
       ("2", "2")''')
db.engine.execute('''DELETE FROM Message''')
db.engine.execute('''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="Message"''')
db.engine.execute('''
INSERT INTO Message ("Text", "Time", "UserId")  
VALUES ("Hello!", "2018-12-18 10:00:00", 1),
       ("Hi!", "2018-12-18 11:00:00", 2)''')

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
        input_user = {'Username': '1', 'Password': '1'}
        expected = {'Id': 1, 'Username': '1', 'Password': '1', 'uri': 'http://localhost/user/1'}
        base64string = base64.encodebytes(('%s:%s' % (input_user['Username'], input_user['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
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
        input_user = {'Username': '1', 'Password': '1'}
        input_query = {'Password': 'first', 'Username': 'first'}
        expected = {'Id': 1, 'Password': 'first', 'Username': 'first', 'uri': 'http://localhost/user/1'}
        base64string = base64.encodebytes(('%s:%s' % (input_user['Username'], input_user['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.put('/user/1',
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(input_query))
        actual = json.loads(response.get_data().decode())
        self.assertDictEqual(
            actual,
            expected
        )

    def test_post_positive_input(self):
        input = {'Username': 'third', 'Password': 'third'}
        base64string = base64.encodebytes(('%s:%s' % (input['Username'], input['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.post('/user/',
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(input))
        actual = response.get_data().decode()
        self.assertTrue('Id' in actual)

class test_integrations_message(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_negative_auth(self):
        expected = 'Unauthorized Access'
        response = self.app.get('/message/',
                                content_type='application/json')
        actual = response.get_data().decode()
        self.assertEqual(
            actual,
            expected
        )

    def test_get_postivie_auth(self):
        input_user = {'Username': '1', 'Password': '1'}
        expected = [
            {'Id': 1, 'Text': 'Hello!', 'Time': '2018-12-18 10:00:00', 'UserId': 1},
            {'Id': 2, 'Text': 'Hi!', 'Time': '2018-12-18 11:00:00', 'UserId': 2}
        ]
        base64string = base64.encodebytes(('%s:%s' % (input_user['Username'], input_user['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.get('/message/',
                                headers=headers,
                                content_type='application/json')
        actual = json.loads(response.get_data().decode())
        self.assertListEqual(
            actual,
            expected
        )

    def test_post_positive_input(self):
        input_user = {'Username': '2', 'Password': '2'}
        input_query = {'Text': 'How are you?', 'Time': '2018-12-18 12:00:00', 'UserId': 2}
        base64string = base64.encodebytes(('%s:%s' % (input_user['Username'], input_user['Password'])).encode('utf8')).decode('utf8').replace('\n', '')
        headers = {'Authorization' : 'Basic %s' % base64string}
        response = self.app.post('/message/',
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(input_query))
        actual = response.get_data().decode()
        self.assertTrue('Id' in actual)
