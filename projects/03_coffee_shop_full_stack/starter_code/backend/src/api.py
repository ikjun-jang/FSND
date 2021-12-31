import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES
'''
Handling GET requests to fetch all drinks
    containing only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or 404 status code indicating entity not found
'''
@app.route("/drinks")
def retrieve_drinks():
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    drinks_list = []
    for drink in drinks:
        drinks_list.append(drink.short())

    return jsonify(
        {
            "success": True, 
            "drinks": drinks_list,
        }
    )

'''
Handling GET requests to fetch all drinks in detail
    it requires the 'get:drinks-detail' permission
    it contains the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or 404 status code indicating entity not found
'''
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def retrieve_drinks_detail(self):
    drinks = Drink.query.all()
    
    if len(drinks) == 0:
        abort(404)

    drinks_list = []
    for drink in drinks:
        drinks_list.append(drink.long())

    return jsonify(
        {
            "success": True, 
            "drinks": drinks_list,
        }
    )

'''
Endpoint to add a new drink
    requiring the 'post:drinks' permission
    containing the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or 422 status code indicating unprocessable entity
'''
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drinks(self):
    body = request.get_json()
    drink_list = []
    
    try:
        new_drink = Drink(
            title = body['title'],
            recipe = json.dumps(body['recipe'])
        )
        new_drink.insert()
        drink_list.append(new_drink.long())
        
        return jsonify(
            {
                "success": True, 
                "drinks": drink_list,
            }
        )
    except:
        abort(422)

'''
Endpoint to edit an existing drink having <id>
    responding with a 404 error if <id> is not found
    updating the corresponding row for <id>
    requiring the 'patch:drinks' permission
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or 422 status code indicating unprocessable entity
'''
@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drinks(self, drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
        
    if drink is None:
        abort(404)

    try:    
        body = request.get_json()
        drink.title = body.get('title')
        drink.recipe = json.dumps(body.get('recipe'))
        drink.update()
        drink_list = []
        drink_list.append(drink.long())
        
        return jsonify(
            {
                "success": True, 
                "drinks": drink_list,
            }
        )
    except:
        abort(422)

'''
Endpoint to delete an existing drink having <id>
    responding with a 404 error if <id> is not found
    deleting the corresponding row for <id>
    requiring the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or 422 status code indicating unprocessable entity
'''
@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(self, drink_id):    
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    
    if drink is None:
        abort(404)

    try:
        drink.delete()
        return jsonify(
            {
                "success": True, 
                "delete": drink.id,
            }
        )
    except:
        abort(422)

# Error Handling
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
Error handler for AuthError Exceptions
A standardized way to communicate auth failure modes
'''
@app.errorhandler(AuthError)
def unauthorized(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response