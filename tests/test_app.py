import os
import unittest

from flaskr import create_app
from flaskr.models import db, insert_dummy_data


class CategoriesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        with self.app.app_context():
            insert_dummy_data(self.app)

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


class AdminTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.token = os.environ.get('ADMIN_JWT')

        with self.app.app_context():
            insert_dummy_data(self.app)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get(self):
        res = self.client().get(
            'api/restaurants',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)

    def test_filter(self):
        res = self.client().get(
            'api/restaurants?user=2',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

    def test_post_success(self):
        res = self.client().post(
            'api/restaurants',
            json={
                'name': 'McDonalds',
                'address': '123 King Street, Toronto, ON',
                'categories': ['Burgers', 'Fast Food'],
                'visited': True,
                'date_visited': 'today'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 3)

    def test_post_error(self):
        # Should fail due to missing restaurant name.
        res = self.client().post(
            'api/restaurants',
            json={
                # 'name': 'McDonalds',
                'address': '123 King Street, Toronto, ON',
                'categories': ['Burgers', 'Fast Food'],
                'visited': True,
                'date_visited': 'today'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch(self):
        res = self.client().patch(
            'api/restaurants/2',
            json={
                'name': 'Burger King',
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('Burger King' in [r['name']
                        for r in data['restaurants']])

    def test_patch_fail(self):
        # should fail due to nonexistent restaurant.
        res = self.client().patch(
            'api/restaurants/999999',
            json={
                'name': 'Burger King',
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete(self):
        res = self.client().delete(
            'api/restaurants/2',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

    def test_delete_fail(self):
        # should fail due to nonexistent restaurant.
        res = self.client().delete(
            'api/restaurants/999999',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


class UserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.token = os.environ.get('USER_JWT')

        with self.app.app_context():
            insert_dummy_data(self.app)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get(self):
        res = self.client().get(
            'api/restaurants',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

    def test_filter_success(self):
        res = self.client().get(
            'api/restaurants?q=foo',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

    def test_filter_fail(self):
        # Normal user shouldn't be able to see other user's data.
        res = self.client().get(
            'api/restaurants?user=1',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_patch_success(self):
        res = self.client().patch(
            'api/restaurants/2',
            json={
                'name': 'Burger King',
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('Burger King' in [r['name']
                        for r in data['restaurants']])

    def test_patch_fail(self):
        # should fail due to restaurant belonging to someone else.
        res = self.client().patch(
            'api/restaurants/1',
            json={
                'name': 'Burger King',
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_fail(self):
        # Normal user does not have permission to delete other's data.
        res = self.client().delete(
            'api/restaurants/1',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()
