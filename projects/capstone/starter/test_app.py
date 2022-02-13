import os
import unittest
import json
import requests
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Club, Player

# variables to access auth0 API
CLIENT_ID = os.getenv('CLIENT_ID', 'xF3XrLq6kJVBcZbl46cSdpewX8BsP8q7')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '5N4eoisQ08u3ljfPMymhx-_-exv6xPRYVZjkwGH-mBYNXdlLpTzZcKzaJ-JPC6HP')
API_AUDIENCE = os.getenv('API_AUDIENCE', 'agency')

# testing user password database:
testingUsers = {
    'contract.assistant@udacity.com': '123abcABC',     #contract assistant (accessible to get:clubs and get:players)
    'contract.manager@udacity.com': '123abcABC',     #contract manager (inaccessible to post:clubs and delete:clubs)
    'executive.director@udacity.com': '123abcABC'  #executive director (accessible to every end point)
}

'''
To get a user access token from user credentials
'''
def getUserToken(userName):
    url = 'https://fsnd3469.us.auth0.com/oauth/token'
    headers = {'content-type': 'application/json'}
    password = testingUsers[userName]
    parameter = { "client_id": CLIENT_ID, 
                  "client_secret": CLIENT_SECRET,
                  "audience": API_AUDIENCE,
                  "grant_type": "password",
                  "username": userName,
                  "password": password, 
                  "scope": "openid" } 
    responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)
    return responseDICT['access_token']

'''
to avoid multiple calls to get a token over many tests
'''
def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper

'''
To make a proper form of header to authorize. A code snippet used from the URL below.
https://stackoverflow.com/questions/48552474/auth0-obtain-access-token-for-unit-tests-in-python
'''
@memoize # memoize code from: https://stackoverflow.com/a/815160
def getUserTokenHeaders(userName='executive.director@udacity.com'):
    return { 'authorization': "Bearer " + getUserToken(userName)} 

class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client

        """ 
        @EDIT: Database credentials handled
        using the dynamic environment variables 
        """
        self.database_path = os.getenv('DATABASE_TEST_URL', "postgresql://postgres:1701@localhost:5432/agency_test")
        if self.database_path.startswith("postgres://"):
            self.database_path = self.database_path.replace("postgres://", "postgresql://", 1)

        setup_db(self.app, self.database_path)

        # to test successful result
        self.new_club = {
            "name": "Inter Milan",
            "category": "Serie A",
            "asset": "$7,000,000,000"
        }

        # to test unsuccessful result
        self.invalid_club = {
            "category": "Serie A",
            "asset": "$7,000,000,000"
        }

        # to test successful result
        self.new_player = {
            "name": "Kevin De Bruyne",
            "value": "110 million euro",
            "club_id": 1
        }

        # to test unsuccessful result
        self.invalid_player = {
            "value": "30 million euro",
            "club_id": "2"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for successful operation and for expected errors.
    """
    def test_create_new_club(self):
        res = self.client().post("/clubs", json=self.new_club, 
            headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_sent_invalid_club_info_to_create(self):
        res = self.client().post("/clubs", json=self.invalid_club, 
            headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_sent_unauthorized_request_to_create_club(self):
        res = self.client().post("/clubs", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_create_new_player(self):
        res = self.client().post("/players", json=self.new_player, 
            headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_sent_invalid_player_info_to_create(self):
        res = self.client().post("/players", json=self.invalid_player, 
            headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_sent_unauthorized_request_to_create_player(self):
        res = self.client().post("/players", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_edit_club(self):
        res = self.client().patch("/clubs/1", json=self.new_club, 
            headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_sent_nonexistent_club_id_to_edit(self):
        res = self.client().patch("/clubs/1000", json=self.invalid_club, 
            headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_403_sent_unauthorized_request_to_edit_club(self):
        res = self.client().patch("/clubs/1", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_edit_player(self):
        res = self.client().patch("/players/4", json=self.new_player, 
            headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_sent_nonexistent_player_id_to_edit(self):
        res = self.client().patch("/players/1000", json=self.invalid_player, 
            headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_403_sent_unauthorized_request_to_edit_player(self):
        res = self.client().patch("/players/4", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_get_players(self):
        res = self.client().get("/players", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_requesting_invalid_address_to_player(self):
        res = self.client().get("/player", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_player(self):
        res = self.client().delete("/players/1", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        player = Player.query.filter(Player.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)
        self.assertEqual(player, None)

    def test_404_if_player_does_not_exist(self):
        res = self.client().delete("/players/1000", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_403_sent_unauthorized_request_to_delete_player(self):
        res = self.client().delete("/players/1", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

    def test_get_clubs(self):
        res = self.client().get("/clubs", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_requesting_invalid_address_to_club(self):
        res = self.client().get("/club", headers=getUserTokenHeaders('contract.assistant@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_club(self):
        res = self.client().delete("/clubs/4", headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)

        club = Club.query.filter(Club.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(club, None)

    def test_404_if_club_does_not_exist(self):
        res = self.client().delete("/clubs/1000", headers=getUserTokenHeaders('executive.director@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_403_sent_unauthorized_request_to_delete_club(self):
        res = self.client().delete("/clubs/4", headers=getUserTokenHeaders('contract.manager@udacity.com'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["code"], "unauthorized")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()