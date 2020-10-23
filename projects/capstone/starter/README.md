# Mentorship Application
## Description:
This API manages a mentorship program. Participants in this program may either be mentors or mentees. Participants may
enroll in one or more projects. There are no restrictions to the number of mentors or mentees per project. An admin has
an almost unlimited access to the API except that they can't rate participants. Users may rate participants,
view participants and projects as well as search for a project by description.
## Getting Started:
### Installing Dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the postgres database

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a database and run the migrations through the following commands:

```bash
createdb mentorship
python manage.py db upgrade
```

## Running the server

To run the server, execute:

```bash
export DATABASE_URL=postgresql://{}:{}@localhost:5432/mentorship
export AUTH0_DOMAIN=meeralsfirstwebapp.us.auth0.com
export ALGORITHMS=['RS256']
export API_AUDIENCE=mentorship
export FLASK_APP=app.py
flask run --reload
```

The `--reload` option will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

## Authentication:

This application uses third party authentication (Auth0)

In order to generate an access token, first you have to sign up to [Auth0](auth0.com)

Your account will need to be assigned a role by the application manager

After you are assigned a role, login from [here](https://meeralsfirstwebapp.us.auth0.com/authorize?audience=mentorship&response_type=token&client_id=phSif85uKU92d8V5wodlpmrMdJqwkr3W&redirect_uri=http://login-completed)

After you complete the login, copy the access_token argument in the url and use it to create requests

The authentication auth0 uses is Bearer token authentication. 

Requests will need to have the following header {"Authentication: Bearer <token>"}

## Testing
All the api endpoints are tested using unittests in test_app.py

First, modify the admin_token and user_token in the MentorshipTestCase class in test_app.py

Second, while the server is running, run the following command
```bash
python test_app.py
```

## Models:
* Participant:

    A participant has a name, skills, and a boolean attribute that determines whether or not they're a mentor
    
    Formatted participant is a dictionary with the following keys: id, name, skills, rating, rated_by, is_mentor
* Project:

    A project has a name, a description, a start date set once it's created and an end date set when its corresponding endpoint is called
    
    Formatted project is a dictionary with thr following keys: id, name, descritpion, start_date, end_date
* Participant_Project Relationship:

    Participants and projects have a many to many relationship. One participant can be enrolled in multiple projects and a single project may have multiple enrolled partiicpants
## Roles:
* Admin:

    Can access all endpoints except PATCH r'/participants/\<int:id>/rate'
* User:

    Can only access the GET endpoints, POST '/projects/search?page=<page_number>' and PATCH r'/participants/\<int:id>/rate'
## Endpoints:
* GET '/mentors?page=<page_number>'

  Fetches paginated mentors with the limit of 10 mentors per page
  
  Request arguments: page number(default=1)
  
  Possible errors: 404 resource not found
  
  Returns: formatted mentors (mentors) and total number of mentors (total_mentors)
* GET '/mentees?page=<page_number>'

  Fetches paginated mentees with the limit of 10 mentees per page
  
  Request arguments: page number(default=1)
  
  Possible errors: 404 resource not found
  
  Returns: formatted mentees (mentees) and total number of mentees (total_mentees)
* GET '/participants?page=<page_number>'

  Fetches paginated participants with the limit of 10 participants per page
  
  Request arguments: page number(default=1)
  
  Possible errors: 404 resource not found
  
  Returns: formatted participants (participants) and total number of participants (total_participants)
* GET '/projects?page=<page_number>'

  Fetches paginated projects with the limit of 10 projects per page
  
  Request arguments: page number(default=1)
  
  Possible errors: 404 resource not found
  
  Returns: formatted projects (projects) and total number of projects (total_projects)
* GET r'/participants/<int:id\>'

  Fetches participant by id
  
  Request arguments: None
  
  Possible errors: 404 resource not found
  
  Returns: formatted participant (participant)
* GET r'/participants/<int:id\>/projects'

  Fetches projects that a certain participant is enrolled in
  
  Possible errors: 404 resource not found
  
  Returns: a list of projects ids(projects)
* GET r'/projects/<int:id\>'

  Fetches project by id
  
  Request arguments: None
  
  Possible errors: 404 resource not found
  
  Returns: formatted participant(participant)
* GET r'/projects/<int:id\>/participants'

  Fetches particpants that are enrolled in a certain project
  
  Request arguments: None
  
  Possible errors: 404 resource not found
  
  Returns: a list of participants ids(participants)
* POST '/projects/search?page=<page_number>' json = {'search_term': \< string: SEARCH_TERM > }

  Fetches pagenated projects that include a certain search term
  
  Request arguments: page number(default=1)
  
  Possible errors: 422 unprocessable or 404 resource not found
  
  Returns: pagenated projects that contain the search term(projects) and total number of projects(total_projects)
* POST '/participants?page=<page_number>' json = {'name': \< string: NAME > , 'skills': \< string: SKILLS > , 'is_mentor': \< bool: IS_MENTOR > }

  Creates a new participant
  
  Request arguments: page number(default=1)
  
  Possible errors: 422 unprocessable
  
  Returns: new participant id(created), formatted pagenated participants(participants) and total number of participants(total_participants)
* POST '/projects' json = {'name': \< string: NAME > , 'description': \< string: DESCRIPTION > }

  Creates a new project
  
  Request arguments: page number(default=1)
  
  Possible errors: 422 unprocessable
  
  Returns: new project id(created), formatted pagenated projects(projects) and total number of projects(total_projects)
* PATCH r'/projects/<int:id\>'

  Sets project end_date to current datetime
  
  Request arguments: None
  
  Possible errors: 404 resource not found
  
  Returns: formatted project(project)
* PATCH '/participants/\<int:id>/rate' json = {'rating': \< int: RATING > }

  Changes participant rating to the average of previous ratings and the new one
  
  Request arguments: None
  
  Possible errors: 422 unprocessable or 404 resource not found
  
  Returns formatted participant(participant)
* PATCH r'participants/<int:participant_id\>/enroll/<int:project_id\>'

  Enrolls a certain participant in a certain project
  
  Request arguments: None
  
  Possible errors: 422 unprocessable or 404 resource not found
  
  Returns: formatted participant(participant)
* DELETE r'participants/<int:id\>'

  Deletes a certain participant
  
  Request arguments: None
  
  Possible errors: 404 resource not found
  
  Returns: deleted participant id(deleted)
* DELETE r'projects/<int:id\>'

  Deletes a certain project
  
  Request arguemnts: None
  
  Possible errors: 404 resource not found
  
  Returns: deletes project id(deleted)
