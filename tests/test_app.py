import unittest

from flaskr import create_app
from flaskr.models import Account, Category, Restaurant, db, insert_dummy_data


class RestoRandoTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()
            insert_dummy_data()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_categories(self):
        res = self.client().get('api/categories')
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 84)

    def test_post_categories(self):
        res = self.client().post('api/categories',
                                 json={'name': 'Chinese American'})
        data = res.json
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])

    def test_resto_by_cat(self):
        res = self.client().get('api/1/restaurants')
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['restaurants'])

    def test_nonexistant_cat(self):
        res = self.client().get('api/99999/restaurants')
        data = res.json
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()
