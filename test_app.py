import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, actors_movies


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.casting_assistant_jwt = os.environ['CASTING_ASSISTANT']
        self.casting_director_jwt = os.environ['CASTING_DIRECTOR']
        self.executive_producer_jwt = os.environ['EXECUTIVE_PRODUCER']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_all_movies_200(self):
        res = self.client().get("/movies", headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_all_actors_200(self):
        res = self.client().get("/actors", headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_add_movie_201(self):
        res = self.client().post("/movies", json={
            "title": "Life of Pi",
            "release_date": "02.28.2012"
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["create"])

    def test_add_actor_201(self):
        res = self.client().post("/actors", json={
            "name": "Ayush Tandon",
            "age": 12,
            "gender": "male"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["create"])

    def test_unauthorized_add_movie_401(self):
        res = self.client().post("/movies", json={
            "title": "Life of Pi",
            "release_date": "28.02.2012"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data['message'], 'Unathorized')

    def test_add_movie_with_wrong_date_format_422(self):
        res = self.client().post("/movies", json={
            "title": "Life of Pi",
            "release_date": "28.02.2012"
        }, headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_add_actor_without_age_parameter_400(self):
        res = self.client().post("/actors", json={
            "name": "Ayush Tandon",
            "gender": "male"
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_update_movie_200(self):
        res = self.client().patch("/movies/2", json={
            "title": "Joker",
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_update_movie_which_does_not_found_404(self):
        res = self.client().patch("/movies/70000", json={
            "title": "Joker",
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data['message'], 'not found')

    def test_update_actor_200(self):
        res = self.client().patch("/actors/2", json={
            "age": 30,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_update_actor_which_does_not_found_404(self):
        res = self.client().patch("/actors/70000", json={
            "age": 30,
        }, headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data['message'], 'not found')

    def test_unauthorized_delete_movie_401(self):
        res = self.client().delete("/movies/1", headers={
            "Authorization": "Bearer {}".format(self.casting_director_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data['message'], 'Unathorized')

    def test_delete_movie_200(self):
        res = self.client().delete("/movies/2", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_delete_actor_200(self):
        res = self.client().delete("/actors/2", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_delete_actor_which_does_not_exist_404(self):
        res = self.client().delete("/actors/10000", headers={
            "Authorization": "Bearer {}".format(self.executive_producer_jwt)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data['message'], 'not found')

if __name__ == "__main__":
    unittest.main()








