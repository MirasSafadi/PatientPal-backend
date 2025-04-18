import unittest
import crypto
from logger import Logger
import jwt
import settings
import utils

class TestApp(unittest.TestCase):

    def setUp(self):
        self.logger = Logger("test_logger")
        self.payload = {"username": "testuser",
                        "hashed_password": "$2b$12$WtlNMmMjzmqjowdlWlhgT./bSuma5b5.Vof3kINY8MKRmaBAueUF."}
        self.token = crypto.generate_token(self.payload)
        self.payload['exp'] = utils.get_utc_now_plus_24_hours()

    def test_when_generate_token_called_token_is_not_None(self):
        self.logger.info("Testing token generation")
        self.logger.info(f"Generated token: {self.token}")
        from app import bcrypt
        self.logger.info(f"token hash: {bcrypt.generate_password_hash(self.token)}")
        self.assertIsNotNone(self.token)

    def test_when_generate_token_called_token_is_valid(self):
        self.logger.info("Testing token validity")
        self.assertEqual(self.payload, jwt.decode(self.token, settings.JWT_SECRET, algorithms=['HS256']))

    def test_when_generate_token_called_token_has_expiration(self):
        self.logger.info("Testing token expiration")
        self.assertIn('exp', jwt.decode(self.token, settings.JWT_SECRET, algorithms=['HS256']))

    # def test_when_decode_invalid_token_exception_raised(self):
    #     self.assertRaises(jwt.exceptions.InvalidSignatureError, jwt.decode(self.token+"dbsfsdfkj", settings.JWT_SECRET, algorithms=['HS256']))
        

    # def test_api_endpoint(self):
    #     response = self.app.get('/api/data')
    #     self.assertEqual(response.status_code, 200)
    #     json_data = response.get_json()
    #     self.assertIn('key', json_data)
    #     self.assertEqual(json_data['key'], 'value')

if __name__ == '__main__':
    unittest.main()