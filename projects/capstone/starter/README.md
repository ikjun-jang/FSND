# Sports Agency Backend

## Introduction
The Sports Agency models a company that creates partnerships with sports clubs and players, whose responsibility is to make contracts between their players and clubs. As an executive director within the company, you can perform every action needed to manage both players and clubs while a contract manager or an assistant can only perform specified actions that their authorities allow.

### Installing Dependencies for the Backend

1. **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


5. **Heroku Setup**
 - Create an account with Heroku [here](https://signup.heroku.com/)
 
 - Download/install the Heroku CLI in order to create our Heroku application and manage it. There are multiple ways to install the Heroku command-line tool, as outlined in the [official installation instructions](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
 
 - Log into heroku with the following command
 ```bash
 heroku login -i
 ```

### Database Setup
With Postgres running, restore a database using the agency.psql file provided. In terminal run:
```bash
psql -d agency -U postgres -a -f agency.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

## Endpoints
### Obtaining an Access Token
- To obtain an Access Token, run the following command and save `access_token` from the result.
```
curl --request POST \
  --url 'https://fsnd3469.us.auth0.com/oauth/token' \
  --header 'content-type: application/json' \
  --data '{"grant_type":"password","client_id":"xF3XrLq6kJVBcZbl46cSdpewX8BsP8q7","client_secret":"5N4eoisQ08u3ljfPMymhx-_-exv6xPRYVZjkwGH-mBYNXdlLpTzZcKzaJ-JPC6HP","audience":"agency","username":"executive.director@udacity.com","password":"123abcABC","scope":"openid"}'
```
### GET /Clubs
- General:
    - Fetches a list of clubs and the corresponding list of players
    - Request Arguments: None
    - Returns: An object with clubs, a total number of clubs
- `curl http://127.0.0.1:8080/clubs -H "authorization: Bearer $ACCESS_TOKEN"`
```
{
  "clubs": [
    {
      "asset": "$7,500,000,000",
      "category": "Premier League",
      "id": 1,
      "name": "Tottenham Hotspur",
      "players": [
        "Harry Kane",
        "Son Heung-Min",
        "Rodrigo Bentancur",
        "Christian Romero"
      ]
    },
    {
      "asset": "$5,500,000,000",
      "category": "Premier League",
      "id": 2,
      "name": "Liverpool FC",
      "players": [
        "Salah",
        "Luis Diaz",
        "Alex Arnold"
      ]
    },
    {
      "asset": "$6,500,000,000",
      "category": "NBA",
      "id": 3,
      "name": "Dallas Mavericks",
      "players": [
        "Luka Doncic",
        "Trey Burke"
      ]
    }
  ],
  "success": true,
  "total_clubs": 3
}
```
### GET /Clubs
- General:
    - Fetches a list of players and the corresponding club
    - Request Arguments: None
    - Returns: An object with players, a total number of players
- `curl http://127.0.0.1:8080/players -H "authorization: Bearer $ACCESS_TOKEN"`
```
{
  "players": [
    {
      "club_id": 2,
      "club_name": "Liverpool FC", 
      "id": 1,
      "name": "Salah",
      "value": "100 million euro"  
    },
    {
      "club_id": 2,
      "club_name": "Liverpool FC",
      "id": 2,
      "name": "Luis Diaz",
      "value": "65 million euro"
    },
    {
      "club_id": 2,
      "club_name": "Liverpool FC",
      "id": 3,
      "name": "Alex Arnold",
      "value": "80 million euro"
    },
    {
      "club_id": 1,
      "club_name": "Tottenham Hotspur",
      "id": 4,
      "name": "Harry Kane",
      "value": "100 million euro"
    },
    {
      "club_id": 1,
      "club_name": "Tottenham Hotspur",
      "id": 5,
      "name": "Son Heung-Min",
      "value": "90 million euro"
    },
    {
      "club_id": 1,
      "club_name": "Tottenham Hotspur",
      "id": 6,
      "name": "Rodrigo Bentancur",
      "value": "50 million euro"
    },
    {
      "club_id": 1,
      "club_name": "Tottenham Hotspur",
      "id": 7,
      "name": "Christian Romero",
      "value": "70 million euro"
    },
    {
      "club_id": 3,
      "club_name": "Dallas Mavericks",
      "id": 8,
      "name": "Luka Doncic",
      "value": "80 million USD"
    },
    {
      "club_id": 3,
      "club_name": "Dallas Mavericks",
      "id": 9,
      "name": "Trey Burke",
      "value": "30 million USD"
    }
  ],
  "success": true,
  "total_players": 9
}
```
### POST /clubs
- General:
    - Sends a post request in order to add a new club
    - Request Body: 
    ```
    {
        "name": "new club name",
        "category": "new club category",
        "asset": "new club asset"
    }
    ```
    - Returns: a single new club object 
```
curl -X POST http://127.0.0.1:8080/clubs \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json"
    -d '{"name":"Inter Milan","category":"Serie A","asset":"$7,000,000,000"}'
```
```
{
  "club": {
    "asset": "$7,000,000,000",
    "category": "Serie A",
    "id": 4,
    "name": "Inter Milan"
  },
  "success": true
}
```
### POST /players
- General:
    - Sends a post request in order to add a new player
    - Request Body: 
    ```
    {
        "name": "new player name",
        "value": "new player value",
        "club_id": "player's club ID"
    }
    ```
    - Returns: a single new player object 
```
curl -X POST http://127.0.0.1:8080/players \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Kevin De Bruyne","value":"110 million euro","club_id":2}'
```
```
{
  "player": {
    "club_id": 2,
    "id": 10,
    "name": "Kevin De Bruyne",
    "value": "110 million euro"
  },
  "success": true
}
```
### PATCH /clubs/${id}
- General:
    - Sends a patch request in order to edit a club
    - Request Body: id - integer
    ```
    {
        "name": "modified club name",
        "category": "modified category",
        "asset": "modified asset value"
    }
    ```
    - Returns: the modified club object 
```
curl -X PATCH http://127.0.0.1:8080/clubs/4 \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"AC Milan","category":"Serie A","asset":"$6,000,000,000"}'
```
```
{
  "clubs": {
    "asset": "$6,000,000,000",
    "category": "Serie A",
    "id": 4,
    "name": "AC Milan"
  },
  "success": true
}
```
### PATCH /players/${id}
- General:
    - Sends a patch request in order to edit a player
    - Request Body: id - integer
    ```
    {
        "name": "modified player name",
        "value": "modified player value",
        "club_id": "modified club ID of the player"
    }
    ```
    - Returns: the modified player object 
```
curl -X PATCH http://127.0.0.1:8080/players/10 \
    -H "authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Lebandovski","value":"120 million euro","club_id":1}'
```
```
{
  "players": {
    "club_id": 1,
    "id": 10,
    "name": "Lebandovski",
    "value": "120 million euro"
  },
  "success": true
}
```
### DELETE /clubs/${id}
- General:
    - Deletes a specified club using the id of the club
    - Request Arguments: id - integer
    - Returns: the appropriate HTTP status code and the id of the deleted question.
- `curl -X DELETE http://127.0.0.1:8080/clubs/4 -H "authorization: Bearer $ACCESS_TOKEN"`
```
{
  "deleted": 4,
  "success": true
}
```
### DELETE /players/${id}
- General:
    - Deletes a specified player using the id of the player
    - Request Arguments: id - integer
    - Returns: the appropriate HTTP status code and the id of the deleted player.
- `curl -X DELETE http://127.0.0.1:8080/players/10 -H "authorization: Bearer $ACCESS_TOKEN"`
```
{
  "deleted": 10, 
  "success": true
}
```
## Roles
- Contract Assistant
    - can `get:clubs` and `get:clubs` 
- Contract Manager
    - can perform all actions except for `post:clubs` and `delete:clubs`
- Executive Director
    - can perform all actions
## Testing
To run the tests, run
```
dropdb agency_test
createdb agency_test
psql -d agency -U postgres -a -f agency.psql
python test_app.py
```