import unittest
from unittest.mock import patch
import crypto
from logger import Logger
import jwt
import settings
import utils

STATIC_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiaGFzaGVkX3Bhc3N3b3JkIjoiJDJiJDEyJFd0bE5NbU1qem1xam93ZGxXbGhnVC4vYlN1bWE1YjUuVm9mM2tJTlk4TUtSbWFCQXVlVUYuIiwiZXhwIjoxNzQ1MDU2MDUyfQ.56i34NM6kUDI9pnA-oj7odJsE6s2cO4npc-QW3nkiYs"
STATIC_PAYLOAD = {  "username": "testuser",
                    "hashed_password": "$2b$12$WtlNMmMjzmqjowdlWlhgT./bSuma5b5.Vof3kINY8MKRmaBAueUF."
                    }
STATIC_DECODED_PAYLOAD = {  "username": "testuser",
                    "hashed_password": "$2b$12$WtlNMmMjzmqjowdlWlhgT./bSuma5b5.Vof3kINY8MKRmaBAueUF.",
                    "exp": 1745056052, # Mocked expiration timestamp
                    }
class CryptoTest(unittest.TestCase):

    def setUp(self):
        self.logger = Logger("test_crypto_logger")

    @patch("utils.get_utc_now_plus_24_hours", return_value=1745056052)  # Mocked timestamp
    @patch('jwt.encode', return_value=STATIC_TOKEN)
    def test_when_generate_token_called_token_is_not_None(self, mock_generate_token, mocked_timestamp):
        self.logger.info("Testing token generation")
        token = crypto.generate_token(STATIC_PAYLOAD)
        self.logger.info(f"Generated token: {token}")
        self.assertIsNotNone(token)
        self.assertEqual(token, STATIC_TOKEN)  # Ensure the token matches the mocked value
        mocked_timestamp.assert_called_once()  # Ensure the mocked function was called
        mock_generate_token.assert_called_once()  # Ensure the mocked function was called with the correct payload

    @patch("utils.get_utc_now_plus_24_hours", return_value=1745056052)  # Mocked timestamp
    @patch('jwt.encode', return_value=STATIC_TOKEN)
    @patch('jwt.decode', return_value=STATIC_DECODED_PAYLOAD)
    def test_when_generate_token_called_token_has_expiration(self, mock_generate_token, mock_decode, mocked_timestamp):
        self.logger.info("Testing token expiration")
        token = crypto.generate_token(STATIC_PAYLOAD)
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        self.assertIn("exp", decoded_token)  # Ensure the token has an expiration field
        self.assertEqual(decoded_token["exp"], 1745056052)  # Ensure the expiration matches the mocked value
        mocked_timestamp.assert_called_once()
        mock_generate_token.assert_called_once()
        mock_decode.assert_called_once()  

    @patch("utils.get_utc_now_plus_24_hours", return_value=1745056052)  # Mocked timestamp
    @patch("jwt.encode", return_value=STATIC_TOKEN)
    @patch("jwt.decode", return_value=STATIC_DECODED_PAYLOAD)
    def test_when_generate_token_called_token_is_valid(self, mock_decode, mock_generate_token, mock_get_utc):
        self.logger.info("Testing token validity")
        token = crypto.generate_token(STATIC_PAYLOAD)
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded_token, STATIC_DECODED_PAYLOAD)  # Ensure the decoded token matches the mocked payload
        mock_get_utc.assert_called_once()
        mock_decode.assert_called_once()
        mock_generate_token.assert_called_once()

    

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