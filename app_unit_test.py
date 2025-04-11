import unittest
from flask import Flask, jsonify
from app import flask_app  # Replace with your actual Flask app instance

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    # def test_api_endpoint(self):
    #     response = self.app.get('/api/data')
    #     self.assertEqual(response.status_code, 200)
    #     json_data = response.get_json()
    #     self.assertIn('key', json_data)
    #     self.assertEqual(json_data['key'], 'value')

if __name__ == '__main__':
    unittest.main()