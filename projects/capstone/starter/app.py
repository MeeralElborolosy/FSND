import os
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Participant, Project, Participant_Project
from auth import requires_auth, AuthError


DATA_PER_PAGE = 10


def pagenate(request, data):
    page_number = request.args.get('page', 1, type=int)
    listed_data = [d.format() for d in data]
    start = (page_number - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    return listed_data[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/mentors')
    @requires_auth('read:participants')
    def read_mentors(payload):
        mentors = Participant.query.filter_by(is_mentor=True).all()
        formatted_mentors = pagenate(request, mentors)
        if len(formatted_mentors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'mentors': formatted_mentors,
            'total_mentors': len(mentors)
        }), 200

    @app.route('/mentees')
    @requires_auth('read:participants')
    def read_mentees(payload):
        mentees = Participant.query.filter_by(is_mentor=False).all()
        formatted_mentees = pagenate(request, mentees)
        if len(formatted_mentees) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'mentees': formatted_mentees,
            'total_mentees': len(mentees)
        }), 200

    @app.route('/participants')
    @requires_auth('read:participants')
    def read_participants(payload):
        participants = Participant.query.all()
        formatted_participants = pagenate(request, participants)
        if len(formatted_participants) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'participants': formatted_participants,
            'total_participants': len(participants)
        }), 200

    @app.route('/projects')
    @requires_auth('read:projects')
    def read_projects(payload):
        projects = Project.query.all()
        formatted_projects = pagenate(request, projects)
        if len(formatted_projects) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'projects': formatted_projects,
            'total_projects': len(projects)
        }), 200

    @app.route('/participants/<int:id>')
    @requires_auth('read:participants')
    def get_participant_by_id(payload, id):
        participant = Participant.query.get(id)
        if participant is None:
            abort(404)
        return jsonify({
            'success': True,
            'participant': participant.format()
        }), 200

    @app.route('/participants/<int:id>/projects')
    @requires_auth('read:participants')
    def get_projects_id_for_a_participant(payload, id):
        participant = Participant.query.get(id)
        if participant is None:
            abort(404)
        projects = Participant_Project.query.filter_by(
            participant_id=id).with_entities(
            Participant_Project.project_id).all()
        return jsonify({
            'success': True,
            'projects': projects
        }), 200

    @app.route('/projects/<int:id>')
    @requires_auth('read:projects')
    def get_project_by_id(payload, id):
        project = Project.query.get(id)
        if project is None:
            abort(404)
        return jsonify({
            'success': True,
            'project': project.format()
        }), 200

    @app.route('/projects/<int:id>/participants')
    @requires_auth('read:projects')
    def get_participants_id_for_a_project(payload, id):
        project = Project.query.get(id)
        if project is None:
            abort(404)
        participants = Participant_Project.query.filter_by(
            project_id=id).with_entities(
            Participant_Project.participant_id).all()
        mentors_count = len(
            Participant.query.filter(
                Participant.id.in_(participants)).filter_by(
                is_mentor=True).all())
        return jsonify({
            'success': True,
            'participants': participants,
            'mentors_count': mentors_count
        }), 200

    @app.route('/projects/search', methods=['POST'])
    @requires_auth('read:projects')
    def search_projects_by_description(payload):
        try:
            data = request.get_json()
            search_term = data.get('search_term', '')
            projects = Project.query.filter(
                Project.description.ilike(
                    '%' + search_term + '%')).all()
            formatted_projects = pagenate(request, projects)
            if len(formatted_projects) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'projects': formatted_projects,
                'total_projects': len(projects)
            }), 200
        except Exception as e:
            if '404 Not Found' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/participants', methods=['POST'])
    @requires_auth('create:participants')
    def create_mentor(payload):
        try:
            data = request.get_json()
            name = data.get('name', '')
            skills = data.get('skills', '')
            is_mentor = data.get('is_mentor')
            participant = Participant(
                name=name, skills=skills, is_mentor=is_mentor)
            participant.insert()
            participants = Participant.query.all()
            formatted_participants = pagenate(request, participants)
            return jsonify({
                'success': True,
                'created': participant.id,
                'participants': formatted_participants,
                'total_participants': len(participants)
            }), 200
        except BaseException:
            abort(422)

    @app.route('/projects', methods=['POST'])
    @requires_auth('create:projects')
    def create_project(payload):
        try:
            data = request.get_json()
            name = data.get('name', '')
            description = data.get('description', '')
            project = Project(name=name, description=description)
            project.insert()
            projects = Project.query.all()
            formatted_projects = pagenate(request, projects)
            return jsonify({
                'success': True,
                'created': project.id,
                'projects': formatted_projects,
                'total_projects': len(projects)
            }), 200
        except BaseException:
            abort(422)

    @app.route('/projects/<int:id>', methods=['PATCH'])
    @requires_auth('create:projects')
    def end_project(payload, id):
        try:
            project = Project.query.get(id)
            if project is None:
                abort(404)
            project.end_date = datetime.datetime.utcnow()
            project.update()
            return jsonify({
                'success': True,
                'project': project.format()
            }), 200
        except Exception as e:
            if '404 Not Found' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/participants/<int:id>/rate', methods=['PATCH'])
    @requires_auth('rate:participants')
    def rate_participant(payload, id):
        try:
            data = request.get_json()
            rating = data.get('rating', 0)
            participant = Participant.query.get(id)
            if participant is None:
                abort(404)
            participant.rating = int(
                (participant.rating * participant.rated_by + rating) /
                (participant.rated_by + 1))
            participant.rated_by = participant.rated_by + 1
            participant.update()
            return jsonify({
                'success': True,
                'participant': participant.format()
            }), 200
        except Exception as e:
            if '404 Not Found' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/participants/<int:participant_id>/enroll/<int:project_id>',
               methods=['PATCH'])
    @requires_auth('enroll:participants')
    def join_project(payload, participant_id, project_id):
        try:
            participant = Participant.query.get(participant_id)
            if participant is None:
                abort(404)
            project = Project.query.get(project_id)
            if project is None:
                abort(404)
            participant.projects.append(project)
            participant.update()
            return jsonify({
                'success': True,
                'participant': participant.format()
            }), 200
        except Exception as e:
            if '404 Not Found' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/participants/<int:id>', methods=['DELETE'])
    @requires_auth('delete:participants')
    def delete_participant(payload, id):
        participant = Participant.query.get(id)
        if participant is None:
            abort(404)
        participant.delete()
        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    @app.route('/projects/<int:id>', methods=['DELETE'])
    @requires_auth('delete:projects')
    def delete_project(payload, id):
        project = Project.query.get(id)
        if project is None:
            abort(404)
        project.delete()
        return jsonify({
            'success': True,
            'deleted': id
        }), 200

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
        }), 400

    @app.errorhandler(500)
    def internal_server_error(request):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()
setup_db(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
