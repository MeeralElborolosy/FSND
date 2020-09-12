# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies


#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Endpoints
* GET '/categories'

    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    - Possible Errors: Resource not found(404) if there are zero categories
    - Example Request:
        ````
        curl http://127.0.0.1:5000/categories
        ````
    - Example response:
        ````
        {
          "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
          },
          "success": true
        }
        ````
* GET '/questions?page=\<page_number>'

    - Fetches pagenated questions
    - Request Arguments: Page number (default is 1)
    - Possible Errors: Resource not found(404) if no questions are found or if the page requested is more than the available pages
    - Returns: An object with keys to questions of the corresponding page limited to the number of questions per page, 
    total number of questions and a dictionary of categories
    - Example Request:
        ````
        curl http://127.0.0.1:5000/questions?page=2
        ````
    - Example Response:
        ````
        {
          "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
          },
          "questions": [
            {
              "answer": "Escher",
              "category": 2,
              "difficulty": 1,
              "id": 16,
              "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {
              "answer": "Mona Lisa",
              "category": 2,
              "difficulty": 3,
              "id": 17,
              "question": "La Giaconda is better known as what?"
            },
            {
              "answer": "One",
              "category": 2,
              "difficulty": 4,
              "id": 18,
              "question": "How many paintings did Van Gogh sell in his lifetime?"
            },
            {
              "answer": "Jackson Pollock",
              "category": 2,
              "difficulty": 2,
              "id": 19,
              "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            },
            {
              "answer": "The Liver",
              "category": 1,
              "difficulty": 4,
              "id": 20,
              "question": "What is the heaviest organ in the human body?"
            },
            {
              "answer": "Alexander Fleming",
              "category": 1,
              "difficulty": 3,
              "id": 21,
              "question": "Who discovered penicillin?"
            },
            {
              "answer": "Blood",
              "category": 1,
              "difficulty": 4,
              "id": 22,
              "question": "Hematology is a branch of medicine involving the study of what?"
            },
            {
              "answer": "Scarab",
              "category": 4,
              "difficulty": 4,
              "id": 23,
              "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            },
            {
              "answer": "Neutral",
              "category": 1,
              "difficulty": 2,
              "id": 29,
              "question": "What's the neutron charge?"
            },
            {
              "answer": "Meeral",
              "category": 4,
              "difficulty": 4,
              "id": 30,
              "question": "What's my name?"
            }
          ],
          "success": true,
          "total_questions": 27
        }
        ````
* DELETE '/questions/\<int:question_id>'

    - Deletes the question with id=question_id
    - Request Arguments: Question ID, Page number(optional)
    - Returns: An object with keys to deleted question id, current total number of questions and list of questions of the
    current page limited to the number of questions per page
    - Possible Errors: Resource not found(404) if the ID requested does not exist
    - Example Request:
        ````
        curl http://127.0.0.1:5000/questions/41 -X DELETE
        ````
    - Example Response:
        ````
        {
          "deleted": 41,
          "questions": [
            {
              "answer": "Maya Angelou",
              "category": 4,
              "difficulty": 2,
              "id": 5,
              "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
              "answer": "Muhammad Ali",
              "category": 4,
              "difficulty": 1,
              "id": 9,
              "question": "What boxer's original name is Cassius Clay?"
            },
            {
              "answer": "Tom Cruise",
              "category": 5,
              "difficulty": 4,
              "id": 4,
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
              "answer": "Edward Scissorhands",
              "category": 5,
              "difficulty": 3,
              "id": 6,
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
              "answer": "Brazil",
              "category": 6,
              "difficulty": 3,
              "id": 10,
              "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
              "answer": "Uruguay",
              "category": 6,
              "difficulty": 4,
              "id": 11,
              "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
              "answer": "George Washington Carver",
              "category": 4,
              "difficulty": 2,
              "id": 12,
              "question": "Who invented Peanut Butter?"
            },
            {
              "answer": "Lake Victoria",
              "category": 3,
              "difficulty": 2,
              "id": 13,
              "question": "What is the largest lake in Africa?"
            },
            {
              "answer": "The Palace of Versailles",
              "category": 3,
              "difficulty": 3,
              "id": 14,
              "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
              "answer": "Agra",
              "category": 3,
              "difficulty": 2,
              "id": 15,
              "question": "The Taj Mahal is located in which Indian city?"
            }
          ],
          "success": true,
          "total_questions": 27
        }
        ````
* POST '/questions'

    - Adds a new question
    - Request Arguments: question data in JSON (question, answer, category_id and difficulty)
    - Possible Errors: Unprocessable(422) if no JSON data was sent with the POST request
    - Returns: An object with keys to created question id, current total number of questions and list of questions of the
    current page limited to the number of questions per page
    - Example Request:
        ````
        curl http://127.0.0.1:5000/questions?page=4 -X POST -H "Content-Type: application/json" -d "{"question": "What is this?", "answer": "This 
        is a question.", "difficulty": 2, "category": 3}"
        ````
        Note: If you're using Windows cmd, add \ before every " inside the json string
        
        Example: ````curl http://127.0.0.1:5000/questions?page=4 -X POST -H "Content-Type: application/json" -d "
        {\"question\":\"What is this?\", \"answer\":\"This is a question.\", \"difficulty\":\"2\", \"category\":\"3\"}" ````
    - Example Response:
        ````
        {
          "created": 47,
          "questions": [
            {
              "answer": "This is a question.",
              "category": 3,
              "difficulty": 2,
              "id": 46,
              "question": "What is this?"
            },
            {
              "answer": "This is a question.",
              "category": 3,
              "difficulty": 2,
              "id": 47,
              "question": "What is this?"
            }
          ],
          "success": true,
          "total_questions": 32
        }
        ````

* POST '/questions/search'
    
    - Searches for a question that includes a certain search term
    - Request Arguments: Search term in JSON
    - Possible Errors: Resource not found(404) if the search term provided does not exist
    - Returns: An object with keys to a list of pagenated questions that include the search term and the total number of 
    questions that include the search term.
    - Example Request:
        ````
        curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "{"searchTerm":"title"}"
        ````
        For Windows cmd: ````curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"title\"}"````
    - Example Response:
    ````
    {
      "questions": [
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
      ],
      "success": true,
      "total_questions": 2
    }
    ````
* GET '/categories/\<int:category_id>/questions'
    
    - Fetches questions from a certain category
    - Request Arguments: ID of the requested category
    - Possible Errors: Resource not found(404) if no questions are found in the requested category
    - Returns: An object with keys to pagenated questions that belong to requested category and the total number of 
    questions that belong to that category
    - Example Request:
        ````
        curl http://127.0.0.1:5000/categories/6/questions
        ````
    - Example Response:
        ````
        {
          "questions": [
            {
              "answer": "Brazil",
              "category": 6,
              "difficulty": 3,
              "id": 10,
              "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
              "answer": "Uruguay",
              "category": 6,
              "difficulty": 4,
              "id": 11,
              "question": "Which country won the first ever soccer World Cup in 1930?"
            }
          ],
          "success": true,
          "total_questions": 2
        }
        ````
        
* POST '/quizzes'
    
    - Fetches a random question that hasn't been fetched before
    - Request Arguments: Two arguments in JSON: List of IDs to previously fetched questions and the category
    from which the questions should be chosen. Category is set to zero if the random question is to be chosen from any category
    - Returns: A random question from specified category or nothing if all questions have been previously fetched
    - Possible Errors: Unprocessable(422) if no JSON data was sent with the POST request
    - Example Request:
        ````
        curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{"previous_questions":[10], "quiz_category":{"id":"6", "type":"Sports"}}"
        ````
        For Windows cmd: ````curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[10], \"quiz_category\":{\"id\":\"6\", \"type\":\"Sports\"}}" ````
    - Example Response:
        ````
        {
          "question": {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
          },
          "success": true
        }
        ````


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
