import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagenate_questions(request, data):
    page_number = request.args.get('page', 1, type=int)
    questions_list = [question.format() for question in data]
    start = (page_number - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return questions_list[start:end]


def format_categories(data):
    formatted_data = {}
    for cat in data:
        formatted_data[cat.id] = cat.type
    return formatted_data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def categories():
        data = Category.query.all()
        if len(data) == 0:
            abort(404)
        formatted_data = format_categories(data)
        result = {
            'categories': formatted_data,
            'success': True
        }
        return jsonify(result)

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions')
    def questions():
        data = Question.query.all()
        formatted_data = pagenate_questions(request, data)
        if len(formatted_data) == 0:
            abort(404)
        categories = format_categories(Category.query.all())
        return jsonify({
            'questions': formatted_data,
            'total_questions': len(data),
            'categories': categories,
            'success': True
        })
    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        data = Question.query.get(question_id)
        questions = Question.query.all()
        formatted_questions = pagenate_questions(request, questions)
        if data is None:
            abort(404)
        data.delete()
        return jsonify({
            'deleted': question_id,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'success': True
        })
    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        try:
            data = request.get_json()
            question_text = data.get('question', '')
            answer_text = data.get('answer', '')
            category = data.get('category', 1)
            difficulty = data.get('difficulty', 1)
            question = Question(
                question=question_text,
                answer=answer_text,
                category=category,
                difficulty=difficulty)
            question.insert()
            questions = Question.query.all()
            formatted_questions = pagenate_questions(request, questions)
            return jsonify({
                'created': question.id,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'success': True
            })
        except BaseException:
            abort(422)

    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.get_json()
        searchTerm = data.get('searchTerm', '')
        data = Question.query.filter(
            Question.question.ilike(
                '%' + searchTerm + '%')).all()
        if len(data) == 0:
            abort(404)
        formatted_questions = pagenate_questions(request, data)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(data)
        })

    '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question_by_category(category_id):
        data = Question.query.filter_by(category=category_id).all()
        if len(data) == 0:
            abort(404)
        formatted_questions = pagenate_questions(request, data)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(data)
        })

    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            data = request.get_json()
            prev = data.get('previous_questions', [])
            category = data.get('quiz_category', {'id': 0})
            if category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=category['id']).all()
            questions = list(filter(lambda q: q.id not in prev, questions))
            if len(questions) == 0:
                return jsonify({
                    'success': True
                })
            else:
                question = random.choice(questions)
                return jsonify({
                    'success': True,
                    'question': question.format()
                })
        except BaseException:
            abort(422)
    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        })

    @app.errorhandler(500)
    def internal_server_error(request):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        })

    return app
