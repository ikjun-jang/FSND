import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
Returns questions to be displayed on current page
'''
def paginated_questions(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

'''
Returns {"id":"type"} formatted dictionary for category
'''
def get_categories():
  categories = Category.query.order_by(Category.id).all()
  categories_dict = {}
  for category in categories:
    categories_dict.update({category.id:category.type})
  return categories_dict

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Allow CORS for every domain and route
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  Setting Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
      "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
    )
    return response

  '''
  Handling GET requests to fetch 
  all available categories.
  '''
  @app.route("/categories")
  def retrieve_categories():
    categories = get_categories()

    if len(categories) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "categories": categories,
      }
    )

  '''
  Handling GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route("/questions")
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginated_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(Question.query.all()),
        "categories": get_categories(),
        "current_category": "All"
      }
    )

  '''
  Endpoint to DELETE question using a question ID. 
  '''
  @app.route("/questions/<int:question_id>", methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginated_questions(request, selection)

      return jsonify(
        {
          "success": True,
          "deleted": question_id,
        }
      )
    except:
      abort(422)

  '''
  Endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  Also, getting questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route("/questions", methods=["POST"])
  def create_questions():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_difficulty = body.get("difficulty", None)
    new_category = body.get("category", None)
    search = body.get("searchTerm", None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(
          Question.question.ilike("%{}%".format(search))
        )
        current_questions = paginated_questions(request, selection)

        return jsonify(
          {
              "success": True,
              "questions": current_questions,
              "total_questions": len(selection.all()),
              "current_category": "All"
          }
        )
      else:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginated_questions(request, selection)

        return jsonify(
          {
              "success": True,
          }
        )
    except:
        abort(422)

  '''
  GET endpoint to get questions based on category. 
  '''
  @app.route("/categories/<int:category_id>/questions")
  def retrieve_questions_by_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginated_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(current_questions),
        "current_category": Category.query.get(category_id).type
      }
    )

  '''
  POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route("/quizzes", methods=["POST"])
  def create_quiz():
    body = request.get_json()

    prev_questions = body.get("previous_questions", None)
    quiz_category = body.get("quiz_category", None)
    category_id = quiz_category.get('id')
    
    if(category_id == 0): # all category
      rand_question = random.choice(Question.query
        .filter(~(Question.id.in_(prev_questions)))
        .all())
    else: # selected category
      rand_question = random.choice(Question.query
        .filter
        (
          Question.category == category_id, 
          ~(Question.id.in_(prev_questions))
        )
        .all())

    if rand_question == None:
      abort(404)

    return jsonify(
      {
        "success": True,
        "question": rand_question.format()
      }
    )

  '''
  Error handlers for all expected errors
  including 400, 404, 422 and 500
  '''
  @app.errorhandler(404)
  def not_found(error):
    return (
      jsonify({"success": False, "error": 404, "message": "resource not found"}),
      404,
    )

  @app.errorhandler(422)
  def unprocessable(error):
    return (
      jsonify({"success": False, "error": 422, "message": "unprocessable"}),
      422,
    )

  @app.errorhandler(400)
  def bad_request(error):
    return (
      jsonify({"success": False, "error": 400, "message": "bad request"}),
      400,
    )

  @app.errorhandler(500)
  def internal_server_error(error):
    return (
      jsonify({"success": False, "error": 500, "message": "internal server error"}),
      500,
    )
  
  return app

    