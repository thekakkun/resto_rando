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
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhyLUhEQmxDZHBDZWZhcVBwRUEyTiJ9.eyJpc3MiOiJodHRwczovL2Rldi0ybTMzcnloMy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1MDY5NGNmYTA4YWYwMDZiODY2YzlmIiwiYXVkIjoicmVzdG8iLCJpYXQiOjE2NTA1NjQ2MjAsImV4cCI6MTY1MDU3MTgyMCwiYXpwIjoieUlwU292Vmp3NWtEY3BBQ3BiUERROUZla2I4a2hST1UiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpteV9yZXN0byIsImdldDpteV9yZXN0byIsInBhdGNoOm15X3Jlc3RvIiwicG9zdDpyZXN0byJdfQ.csibj5XBv4_9KgQjczZabsWgiDTR7OKaxdun4wUQZryVDt2H0_XX20ik7xSTqueDuCpRXgNY75RWNJiiFM44TWGRiBhvFZWikPp20QcVwKnPRaRnnj7h6OZhsbWsYCMYxEBNpPSV6slZtkt2JNEXOCaZIw_t3V4oKKE2s5xrPC23MggRGSuodz9tJN8GhSstdtUIFFqNrrF91ypUdR6tosOMik_Ni5w6d-erGlcDlBGkbM6L32z5vXYYl_oTYbBSMHbc0pt82gNpTbDBRfUzBes8rdAMzVilZAhxPcPr_r-LobmATH7Cj1BJriZQ-f_3rGwqqZ1-zFKqxCpR9HjV0w'

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
