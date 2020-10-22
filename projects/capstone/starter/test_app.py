import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Participant, Project


class MentorshipTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.username = "postgres"
        self.password = "899162mm*"
        self.database_name = "mentorship"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.username, self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_project = {
            'name': 'Test_Project',
            'description': 'This is a test project.'
        }
        self.new_participant = {
            'name': 'Meeral',
            'skills': 'Programming',
            'is_mentor': False
        }
        self.selected_participant_id = 30
        self.selected_project_id = 32
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllITVdXZjF4X19aU3FOMWd1dDVEYiJ9.eyJpc3MiOiJodHRwczovL21lZXJhbHNmaXJzdHdlYmFwcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTMxNjU3NDgyMjEzMzE3NTM1NzIiLCJhdWQiOlsibWVudG9yc2hpcCIsImh0dHBzOi8vbWVlcmFsc2ZpcnN0d2ViYXBwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDMzNTA2NzQsImV4cCI6MTYwMzQzNzA3NCwiYXpwIjoicGhTaWY4NXVLVTkyZDhWNXdvZGxwbXJNZEpxd2tyM1ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOnBhcnRpY2lwYW50cyIsImNyZWF0ZTpwcm9qZWN0cyIsImRlbGV0ZTpwYXJ0aWNpcGFudHMiLCJkZWxldGU6cHJvamVjdHMiLCJlbnJvbGw6cGFydGljaXBhbnRzIiwicmVhZDpwYXJ0aWNpcGFudHMiLCJyZWFkOnByb2plY3RzIl19.XSgPoLeMy4WtuWeJtNrV2BOjSxiqjugB7U12qy7SzWS0THjPE03gex92uoRYv7dJ5I-vvr5ojmZL1-awq_WA41Htx6pLbZnyQSk9asky0hKD-N8CJNiWykI3Bo1A3D3SaYc4C8EbSaPPi0OcP4W8VX7N_5YDPMjcIwAwiSpHLwkeWS0UxDpQyyqXqUphrvRAiX1enD4pJibq06_tSUtBTn8xx65fY2ubN7ygC8uVKr5IiKovNARWMZkwwKK3CyY-AS2zo0eXZ6ck2cTH9KK4h5kuTFk8HZZHZWS4V06EKFML0w7BNOv_64fiSXwMt622iUvuuiYynq96CcRFIGFzjg'
        self.user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllITVdXZjF4X19aU3FOMWd1dDVEYiJ9.eyJpc3MiOiJodHRwczovL21lZXJhbHNmaXJzdHdlYmFwcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkxMjkzMzA4MTUwNzA2MzkxMzgiLCJhdWQiOlsibWVudG9yc2hpcCIsImh0dHBzOi8vbWVlcmFsc2ZpcnN0d2ViYXBwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDMzNTA2ODIsImV4cCI6MTYwMzQzNzA4MiwiYXpwIjoicGhTaWY4NXVLVTkyZDhWNXdvZGxwbXJNZEpxd2tyM1ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicmF0ZTpwYXJ0aWNpcGFudHMiLCJyZWFkOnBhcnRpY2lwYW50cyIsInJlYWQ6cHJvamVjdHMiXX0.McAhkRFN8LRCZw5aklbm8xAJffIrYcw9XlNTJQlrr1ZfbcK0CtC8VwXlBlBSwo5-GbPas8FaGC5SO53jnW9VqkpjSNQndO7eGu1-oiQ0crAxpRMVjz5-wz8nEXWR6cEvgRLEplvTFSv1ISFWLhzf7vqEYtf2CEJSr6KCk8pDfYu9SNwDe5-RNxcT0Su8hI7g6YaoNJ47QE2MLjtuWqyV6UCSbZSDrsg15c1ECJvFFKOTJC_sOqsz0hM1A15b_9wxzDo9ZMVQpjrX3SWTrBFCQp8arDqdMddrFgkINfbSht63f7EBxTyuKqi8YLpViTZWcQb3zDVykgWzx0GTQNRe_w'
        self.admin_header = {'Authorization': 'Bearer '+ self.admin_token}
        self.user_header = {'Authorization': 'Bearer '+ self.user_token}
        self.deleted_project_id = 16
        self.deleted_participant_id = 16
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_mentors(self):
        res = self.client().get('/mentors', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['mentors'])

    def test_404_if_mentors_page_doesnt_exist(self):
        res = self.client().get('/mentors?page=1000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_mentees(self):
        res = self.client().get('/mentees', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['mentees'])

    def test_404_if_mentees_page_doesnt_exist(self):
        res = self.client().get('/mentees?page=1000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants(self):
        res = self.client().get('/participants', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participants'])

    def test_404_if_participants_page_doesnt_exist(self):
        res = self.client().get('/participants?page=1000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects(self):
        res = self.client().get('/projects', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_404_if_projects_page_doesnt_exist(self):
        res = self.client().get('/projects?page=1000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants_by_id(self):
        res = self.client().get('/participants/'+str(self.selected_participant_id), headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_404_if_participant_id_doesnt_exist(self):
        res = self.client().get('/participants/10000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects_for_a_participant(self):
        res = self.client().get('/participants/'+str(self.selected_participant_id)+'/projects', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_404_if_participant_id_doesnt_exist_in_get_projects_for_a_participant(self):
        res = self.client().get('/participants/10000/projects', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects_by_id(self):
        res = self.client().get('/projects/'+str(self.selected_project_id), headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_project_id_doesnt_exist(self):
        res = self.client().get('/projects/10000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants_for_a_projects(self):
        res = self.client().get('/projects/'+str(self.selected_project_id)+'/participants', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participants'])
        self.assertTrue(data['mentors_count'])

    def test_404_if_project_id_doesnt_exist_in_get_participants_for_a_projects(self):
        res = self.client().get('/projects/10000/participants', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_participant(self):
        res = self.client().post('/participants', json=self.new_participant, headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_participants'])
        self.assertTrue(len(data['participants']))
        self.assertTrue(data['created'])
        test_id = data['created']
        participant = Participant.query.filter(Participant.id == test_id).one_or_none()
        self.assertNotEqual(participant, None)

    def test_422_if_create_participant_failed(self):
        res = self.client().post('/participants', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_project(self):
        res = self.client().post('/projects', json=self.new_project, headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_projects'])
        self.assertTrue(len(data['projects']))
        self.assertTrue(data['created'])
        test_id = data['created']
        project = Project.query.filter(Project.id == test_id).one_or_none()
        self.assertNotEqual(project, None)

    def test_422_if_create_project_failed(self):
        res = self.client().post('/projects', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_end_project(self):
        res = self.client().patch('/projects/'+str(self.selected_project_id), headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_end_project_not_found(self):
        res = self.client().patch('/projects/10000', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_search_project(self):
        res = self.client().post('/projects/search', json={'search_term': 'test'}, headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['projects']))
        self.assertTrue(data['total_projects'])

    def test_search_project_if_search_term_empty(self):
        res = self.client().post('/projects/search', json={}, headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['projects']))
        self.assertTrue(data['total_projects'])

    def test_422_if_search_project_failed(self):
        res = self.client().post('/projects/search', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_if_search_project_no_results(self):
        res = self.client().post('/projects/search', json={'search_term': 'lalalalalalala'}, headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_rate_participant(self):
        res = self.client().patch('/participants/'+str(self.selected_participant_id)+'/rate', json={'rating': 3}, headers = self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_404_if_rate_participant_not_found(self):
        res = self.client().patch('/participants/10000/rate', json={'rating': 3}, headers = self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_if_rate_participant_with_rating_empty(self):
        res = self.client().patch('/participants/'+str(self.selected_participant_id)+'/rate', headers = self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_enroll_participant(self):
        res = self.client().patch('/participants/'+str(self.selected_participant_id)+'/enroll/'+str(self.selected_project_id), headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_404_if_enroll_participant_has_invalid_participant_id(self):
        res = self.client().patch('/participants/10000/enroll/'+str(self.selected_project_id), headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_enroll_participant_has_invalid_project_id(self):
        res = self.client().patch('/participants/'+str(self.selected_participant_id)+'/enroll/10000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_participant(self):
        res = self.client().delete('/participants/' + str(self.deleted_participant_id), headers = self.admin_header)
        data = json.loads(res.data)
        participant = Participant.query.filter(Participant.id == self.deleted_participant_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.deleted_participant_id)

    def test_404_if_delete_participant_not_found(self):
        res = self.client().delete('/participants/10000', headers = self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_project(self):
        res = self.client().delete('/projects/' + str(self.deleted_project_id), headers = self.admin_header)
        data = json.loads(res.data)
        project = Project.query.filter(Project.id == self.deleted_project_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.deleted_project_id)

    def test_404_if_delete_project_not_found(self):
        res = self.client().delete('/projects/10000', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
