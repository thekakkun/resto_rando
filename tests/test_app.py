import json
import unittest

from flaskr import create_app
from flaskr.models import Account, Category, Restaurant, db, insert_dummy_data


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
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhyLUhEQmxDZHBDZWZhcVBwRUEyTiJ9.eyJpc3MiOiJodHRwczovL2Rldi0ybTMzcnloMy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1MDY5MmExN2FiYjkwMDY5ZWZiNGEyIiwiYXVkIjoicmVzdG8iLCJpYXQiOjE2NTA1NjI2NjcsImV4cCI6MTY1MDU2OTg2NywiYXpwIjoieUlwU292Vmp3NWtEY3BBQ3BiUERROUZla2I4a2hST1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphbnlfcmVzdG8iLCJkZWxldGU6bXlfcmVzdG8iLCJnZXQ6YW55X3Jlc3RvIiwiZ2V0Om15X3Jlc3RvIiwicGF0Y2g6YW55X3Jlc3RvIiwicGF0Y2g6bXlfcmVzdG8iLCJwb3N0OnJlc3RvIl19.hnUjAmUlYSyu2Z5lMuTmpwvOzNYt_0KC1C6X2vTrSMTtGDSDBNRkNH76Rn34ggQ5jTGb_r_GhAb-_bcAHnq-obn22IsuSq-rekmYO4qy7i98Ofn_g4eyK16HT2iqmg7oGTmAff9EMVuqnTFDt1uAJdTcpzbUrChQrT9KYEmlTb4eTivq4NPi30DlDVkEfb_yL7biaMDfHymaWLYuxGUNnbENA_LkEb1niI6D811sEbETuwTFI8M-DH6BAj-oyRsrN04oQmOnzIWY69lZgX_IDiMhKXokHFtT67bmZXHy3w-BhB9Ki3U5dwAQUfR4xCPrxLCpCcIfi2tS6faQAZLijQ'

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

    def test_patch_nonexistent(self):
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

    def test_delete_nonexistent(self):
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
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhyLUhEQmxDZHBDZWZhcVBwRUEyTiJ9.eyJpc3MiOiJodHRwczovL2Rldi0ybTMzcnloMy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1MDY5NGNmYTA4YWYwMDZiODY2YzlmIiwiYXVkIjoicmVzdG8iLCJpYXQiOjE2NTA1NTQ4MDksImV4cCI6MTY1MDU2MjAwOSwiYXpwIjoieUlwU292Vmp3NWtEY3BBQ3BiUERROUZla2I4a2hST1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpteV9yZXN0byIsImdldDpteV9yZXN0byIsInBhdGNoOm15X3Jlc3RvIiwicG9zdDpyZXN0byJdfQ.r7nmuh6MyD8BaxASWLrDb8_FxwEYImX7mgabDFLkfLzkCvymPw0Ny9EPEE2CpzKIDxBBZkNdRCNOhSDQkAjAOglrpxnjWLyf-o3JGuil6z9mqrtghIyA7HH7uaM8ephulYzL5zsl8UDnVUKA-yCzk8RyR0-ELTUGcCBFxqv6limIAjaaSRh8KUOMPhPfzQlagZ5w0ecytotSptNYe_jKsICJGaeWTqX1wA7aTgLHR3lEuU4ejT_z0NMntPNEFq_-FHvBZ8D8MRmVd9L_PfwhoRo5LJ_R-iKhhKvhl6t_dDQBLBLlY33hwf9W3oavlxzj76eNIQC3RBKFMVdaQKczGQ'

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
        self.assertEqual(len(data['restaurants']), 1)

    def test_filter(self):
        res = self.client().get(
            'api/restaurants?user=1',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        data = res.json
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_post(self):
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
        self.assertEqual(len(data['restaurants']), 2)


if __name__ == '__main__':
    unittest.main()
