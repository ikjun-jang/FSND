import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Club, Player
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  Handling GET requests to fetch 
  all available clubs
  This endpoint should return a list of clubs, 
  number of total clubs
  '''
  @app.route("/clubs")
  @requires_auth("get:clubs")
  def retrieve_clubs(self):
    clubs = Club.query.all()
    club_list = []

    if len(clubs) == 0:
      abort(404)

    '''
    adding a list of player names to each club
    '''
    for club in clubs:
      players = Player.query.filter(Player.club_id==club.id).all()
      club_dic = club.format()
      club_dic['players'] = [p.name for p in players]
      club_list.append(club_dic)

    return jsonify(
      {
        "success": True,
        "clubs": club_list,
        "total_clubs": len(clubs)
      }
    )

  '''
  Handling GET requests for players
  This endpoint should return a list of players, 
  number of total players
  '''
  @app.route("/players")
  @requires_auth("get:players")
  def retrieve_players(self):
    players = Player.query.all()
    player_list = []

    if len(players) == 0:
      abort(404)

    '''
    adding club name to each player
    '''
    for player in players:
      club = Club.query.filter(Club.id==player.club_id).one_or_none()
      player_dic = player.format()
      player_dic["club_name"] = club.name
      player_list.append(player_dic)

    return jsonify(
      {
        "success": True,
        "players": player_list,
        "total_players": len(players)
      }
    )

  '''
  Endpoint to POST a new club, 
  which will require club name, category and asset
  '''
  @app.route("/clubs", methods=["POST"])
  @requires_auth("post:clubs")
  def create_clubs(self):
    body = request.get_json()

    try:
      new_club = Club(
        name = body['name'],
        category = body['category'],
        asset = body['asset']
      )
      new_club.insert()

      return jsonify(
        {
          "success": True,
          "club": new_club.format()
        }
      )
    except:
      abort(422)

  '''
  Endpoint to POST a new player, 
  which will require player name, value and club ID
  '''
  @app.route("/players", methods=["POST"])
  @requires_auth("post:players")
  def create_players(self):
    body = request.get_json()

    try:
      new_player = Player(
        name = body['name'],
        value = body['value'],
        club_id = body['club_id']
      )
      new_player.insert()

      return jsonify(
        {
          "success": True,
          "player": new_player.format()
        }
      )
    except:
      abort(422)

  '''
  Endpoint to EDIT a club, 
    returns the updated club info.
  '''
  @app.route("/clubs/<int:club_id>", methods=["PATCH"])
  @requires_auth("patch:clubs")
  def update_clubs(self, club_id):
    club = Club.query.filter(Club.id==club_id).one_or_none()

    if club is None:
      abort(404)

    try:
      body = request.get_json()
      club.name = body['name']
      club.category = body['category']
      club.asset = body['asset']
      club.update()

      return jsonify(
        {
          "success": True,
          "clubs": club.format()
        }
      )
    except:
      abort(422)

  '''
  Endpoint to EDIT a player, 
    returns the updated player info.
  '''
  @app.route("/players/<int:player_id>", methods=["PATCH"])
  @requires_auth("patch:players")
  def update_players(self, player_id):
    player = Player.query.filter(Player.id==player_id).one_or_none()

    if player is None:
      abort(404)

    try:
      body = request.get_json()
      player.name = body['name']
      player.value = body['value']
      player.club_id = body['club_id']
      player.update()

      return jsonify(
        {
          "success": True,
          "players": player.format()
        }
      )
    except:
      abort(422)

  '''
  Endpoint to DELETE club using a club ID. 
  '''
  @app.route("/clubs/<int:club_id>", methods=["DELETE"])
  @requires_auth("delete:clubs")
  def delete_clubs(self, club_id):
    club = Club.query.filter(Club.id==club_id).one_or_none()

    if club is None:
      abort(404)

    try:
      club.delete()
      return jsonify(
        {
          "success": True,
          "deleted": club.id
        }
      )
    except:
      abort(422)

  '''
  Endpoint to DELETE player using a player ID. 
  '''
  @app.route("/players/<int:player_id>", methods=["DELETE"])
  @requires_auth("delete:players")
  def delete_players(self, player_id):
    player = Player.query.filter(Player.id==player_id).one_or_none()

    if player is None:
      abort(404)

    try:
      player.delete()
      return jsonify(
        {
          "success": True,
          "deleted": player.id
        }
      )
    except:
      abort(422)

  # Error Handling
  '''
  Error handling for bad request
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  '''
  Error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  '''
  Error handler for entity not found
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404
  
  '''
  Error handler for internal server error
  '''
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
      }), 500

  '''
  Error handler for AuthError Exceptions
  A standardized way to communicate auth failure modes
  '''
  @app.errorhandler(AuthError)
  def unauthorized(ex):
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run()