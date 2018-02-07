# tests/test_user.py

import os

import unittest
import json

from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """test case for the model user"""

    def setUp(self):
        """define test variable and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {'email': 'test@poaegis.com', 'password': 'test123'}
        
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    
    def test_user_registration(self):
        """test case for user registration"""
        res = self.client().post('/auth/register', data=self.user_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)


    def test_user_already_registered(self):
        """ test case for duplicated registering activity"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "You already registered.")


if __name__ == "__main__":
    unittest.main()
