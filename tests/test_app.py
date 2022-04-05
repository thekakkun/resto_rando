import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr.api import app
from flaskr.models import Account, Category, Restaurant, db


class RestoRandoTest(unittest.TestCase):

    def setUp(self):
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_NAME = 'resto_rando_test'
        self.database_path = f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5432/{self.DB_NAME}'

        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app
        db.init_app(self.app)

        # self.app = app.test_client()
        # db.init_app(self.app)
        db.drop_all()
        db.create_all()

        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     self.db.create_all()

    def tearDown(self):
        pass

    def test_get_categories(self):
        res = self.app.get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
