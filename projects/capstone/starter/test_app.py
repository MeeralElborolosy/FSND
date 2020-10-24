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
        self.database_path = os.getenv('DATABASE_URL')
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
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI' \
                           '6IllITVdXZjF4X19aU3FOMWd1dDVEYiJ9.eyJpc3MiO' \
                           'iJodHRwczovL21lZXJhbHNmaXJzdHdlYmFwcC51cy5h' \
                           'dXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnw' \
                           'xMTMxNjU3NDgyMjEzMzE3NTM1NzIiLCJhdWQiOlsibW' \
                           'VudG9yc2hpcCIsImh0dHBzOi8vbWVlcmFsc2ZpcnN0d' \
                           '2ViYXBwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJp' \
                           'YXQiOjE2MDM1MDI0ODYsImV4cCI6MTYwMzU4ODg4Niw' \
                           'iYXpwIjoicGhTaWY4NXVLVTkyZDhWNXdvZGxwbXJNZE' \
                           'pxd2tyM1ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlI' \
                           'GVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOnBh' \
                           'cnRpY2lwYW50cyIsImNyZWF0ZTpwcm9qZWN0cyIsImR' \
                           'lbGV0ZTpwYXJ0aWNpcGFudHMiLCJkZWxldGU6cHJvam' \
                           'VjdHMiLCJlbnJvbGw6cGFydGljaXBhbnRzIiwicmVhZ' \
                           'DpwYXJ0aWNpcGFudHMiLCJyZWFkOnByb2plY3RzIl19' \
                           '.daW63fl2a2zVtNxWAapUhGzGA68BahYr8WP2MuRcnf' \
                           'pftkRhfIOKwqTfd3UyDji4Gb39DdIHO1-QKQh7kjluM' \
                           'JdekDpCfLWslIPmokpxHDOJGr98JE56cepWeE_V5XcA' \
                           'pI1nh0dnXhOkDeeeb5y3upsXlROsJx-8q1HUhjZ0CAb' \
                           'A0Wi3L1sYtUmpsyhbYv9PYtikZTsFv0ofaumBg9b1C6' \
                           '43BIpTtg08Flh3g0fnPav-Yw8wi_a4SWn3mj4zBw2E1' \
                           '_zA60q4sY9Hea90JrFaU_1EfGIhLpE1nDsphKe_JRqO' \
                           'J6mdy3ZKfTBVnfU2qA6Lk3jY_vJsSVtIERwlL8bfnA'
        self.user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI' \
                          '6IllITVdXZjF4X19aU3FOMWd1dDVEYiJ9.eyJpc3MiO' \
                          'iJodHRwczovL21lZXJhbHNmaXJzdHdlYmFwcC51cy5h' \
                          'dXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnw' \
                          'xMDkxMjkzMzA4MTUwNzA2MzkxMzgiLCJhdWQiOlsibW' \
                          'VudG9yc2hpcCIsImh0dHBzOi8vbWVlcmFsc2ZpcnN0d' \
                          '2ViYXBwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJp' \
                          'YXQiOjE2MDM1MDI2MDYsImV4cCI6MTYwMzU4OTAwNiw' \
                          'iYXpwIjoicGhTaWY4NXVLVTkyZDhWNXdvZGxwbXJNZE' \
                          'pxd2tyM1ciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlI' \
                          'GVtYWlsIiwicGVybWlzc2lvbnMiOlsicmF0ZTpwYXJ0' \
                          'aWNpcGFudHMiLCJyZWFkOnBhcnRpY2lwYW50cyIsInJ' \
                          'lYWQ6cHJvamVjdHMiXX0.fzZkrGdTSMEbVOPYPbG28X' \
                          'EOJRMyWepxjBN6IYOxFgHBG1QNiHey-61LiQFGyxA32' \
                          'GwIaNyWFQ80-57tIc6s6vVnEGNxJDG0pU05D7aVsIbN' \
                          'KZtt3OQ7WowmLdc1fTjd0eyQ_39zOyzn2vLJY9ytEvl' \
                          'wABwXx3FeMjW1uOkF02fRc5_9xvyK6fiEAyFWJ-J14d' \
                          'qFlZ49k6-jC8m9N8-8h5d96hfnuMapqLhcvrmvKvhdy' \
                          '-0368oWGy7-N1HULT0emHM773GF6aIODGXk1Mplf6pl' \
                          'moRpHhZGb3KP024oGsGLewH8PkRHj2abvyFGcchu0y4' \
                          'o-d63-M2v-gXIdA4wFw'
        self.admin_header = {'Authorization': 'Bearer ' + self.admin_token}
        self.user_header = {'Authorization': 'Bearer ' + self.user_token}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            dummy_participant_delete = Participant(
                name='dummy', skills='dummy', is_mentor=True)
            dummy_mentor_populate = Participant(
                name='Meeral', skills='Programming', is_mentor=True)
            dummy_mentee_populate = Participant(
                name='Tofy', skills='Gaming', is_mentor=False)
            dummy_project_delete = Project(name='dummy', description='dummy')
            dummy_project_populate = Project(name='dummy', description='dummy')
            dummy_mentee_populate.projects.append(dummy_project_populate)
            dummy_mentor_populate.projects.append(dummy_project_populate)
            self.db.session.add(dummy_project_delete)
            self.db.session.add(dummy_project_populate)
            self.db.session.add(dummy_participant_delete)
            self.db.session.add(dummy_mentor_populate)
            self.db.session.add(dummy_mentee_populate)
            self.db.session.commit()
            self.deleted_participant_id = dummy_participant_delete.id
            self.deleted_project_id = dummy_project_delete.id
            self.unauthorized_delete_participant_id = dummy_mentee_populate.id
            self.selected_participant_id = dummy_mentor_populate.id
            self.selected_project_id = dummy_project_populate.id

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_mentors(self):
        res = self.client().get('/mentors', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['mentors'])

    def test_404_if_mentors_page_doesnt_exist(self):
        res = self.client().get('/mentors?page=1000', headers=self.admin_header
                                )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_mentees(self):
        res = self.client().get('/mentees', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['mentees'])

    def test_404_if_mentees_page_doesnt_exist(self):
        res = self.client().get('/mentees?page=1000', headers=self.admin_header
                                )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants(self):
        res = self.client().get('/participants', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participants'])

    def test_404_if_participants_page_doesnt_exist(self):
        res = self.client().get('/participants?page=1000',
                                headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects(self):
        res = self.client().get('/projects', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_404_if_projects_page_doesnt_exist(self):
        res = self.client().get('/projects?page=1000',
                                headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants_by_id(self):
        res = self.client().get('/participants/' +
                                str(self.selected_participant_id),
                                headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_404_if_participant_id_doesnt_exist(self):
        res = self.client().get('/participants/10000',
                                headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects_for_a_participant(self):
        res = self.client().get('/participants/' +
                                str(self.selected_participant_id) +
                                '/projects', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['projects'])

    def test_404_if_participant_doesnt_exist_in_get_projects_for_a_participant(
            self):
        res = self.client().get(
            '/participants/10000/projects',
            headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_projects_by_id(self):
        res = self.client().get('/projects/' +
                                str(self.selected_project_id),
                                headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    def test_404_if_project_id_doesnt_exist(self):
        res = self.client().get('/projects/10000', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_participants_for_a_projects(self):
        res = self.client().get('/projects/' + str(self.selected_project_id) +
                                '/participants', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participants'])
        self.assertTrue(data['mentors_count'])

    def test_404_if_project_id_doesnt_exist_in_get_participants_for_a_projects(
            self):
        res = self.client().get(
            '/projects/10000/participants',
            headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_participant(self):
        res = self.client().post(
            '/participants',
            json=self.new_participant,
            headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_participants'])
        self.assertTrue(len(data['participants']))
        self.assertTrue(data['created'])
        test_id = data['created']
        participant = Participant.query.filter(
            Participant.id == test_id).one_or_none()
        self.assertNotEqual(participant, None)

    def test_422_if_create_participant_failed(self):
        res = self.client().post('/participants', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_project(self):
        res = self.client().post(
            '/projects',
            json=self.new_project,
            headers=self.admin_header)
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
        res = self.client().post('/projects', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_end_project(self):
        res = self.client().patch('/projects/' +
                                  str(self.selected_project_id),
                                  headers=self.admin_header)
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
        res = self.client().post(
            '/projects/search',
            json={
                'search_term': 'test'},
            headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['projects']))
        self.assertTrue(data['total_projects'])

    def test_search_project_if_search_term_empty(self):
        res = self.client().post('/projects/search', json={},
                                 headers=self.admin_header)
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
        res = self.client().post(
            '/projects/search',
            json={
                'search_term': 'lalalalalalala'},
            headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_rate_participant(self):
        res = self.client().patch('/participants/' +
                                  str(self.selected_participant_id) +
                                  '/rate', json={'rating': 3},
                                  headers=self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_403_if_unauthorized_rate(self):
        res = self.client().patch('/participants/' +
                                  str(self.selected_participant_id) +
                                  '/rate', json={'rating': 3},
                                  headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_if_rate_participant_not_found(self):
        res = self.client().patch(
            '/participants/10000/rate',
            json={
                'rating': 3},
            headers=self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_if_rate_participant_with_rating_empty(self):
        res = self.client().patch('/participants/' +
                                  str(self.selected_participant_id) +
                                  '/rate', headers=self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_enroll_participant(self):
        res = self.client().patch('/participants/' +
                                  str(self.selected_participant_id) +
                                  '/enroll/' + str(self.selected_project_id),
                                  headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['participant'])

    def test_404_if_enroll_participant_has_invalid_participant_id(self):
        res = self.client().patch('/participants/10000/enroll/' +
                                  str(self.selected_project_id),
                                  headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_enroll_participant_has_invalid_project_id(self):
        res = self.client().patch('/participants/' +
                                  str(self.selected_participant_id) +
                                  '/enroll/10000', headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_participant(self):
        res = self.client().delete('/participants/' +
                                   str(self.deleted_participant_id),
                                   headers=self.admin_header)
        data = json.loads(res.data)
        participant = Participant.query.filter(
            Participant.id == self.deleted_participant_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.deleted_participant_id)

    def test_404_if_delete_participant_not_found(self):
        res = self.client().delete('/participants/10000',
                                   headers=self.admin_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_403_if_unauthorized_delete(self):
        res = self.client().delete('/participants/' +
                                   str(self.unauthorized_delete_participant_id
                                       ), headers=self.user_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_project(self):
        res = self.client().delete('/projects/' +
                                   str(self.deleted_project_id),
                                   headers=self.admin_header)
        data = json.loads(res.data)
        project = Project.query.filter(
            Project.id == self.deleted_project_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], self.deleted_project_id)

    def test_404_if_delete_project_not_found(self):
        res = self.client().delete('/projects/10000', headers=self.admin_header
                                   )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
