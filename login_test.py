import unittest
from app import flask_app, bcrypt
from mongodb_interface import MongoDBInterface
from logger import Logger  # ייבוא הלוגר

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.logger = Logger("test-login")  # יצירת logger
        self.app = flask_app.test_client()
        self.app.testing = True
        self.db = MongoDBInterface()
        self.db.connect()
        self.logger.info("Connected to test database")

        # יצירת משתמש לבדיקה (אם לא קיים)
        username = "testuser"
        password = "testpass"
        existing_user = self.db.get_document("users", {"username": username})
        if not existing_user:
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            self.db.add_document("users", {"username": username, "password": hashed})
            self.logger.info("Test user created")
        else:
            self.logger.info("Test user already exists")

        self.test_credentials = {
            "username": "testuser",
            "password": "testpass"
        }

    def test_login_success(self):
        self.logger.debug("Testing successful login")
        response = self.app.post('/login', data=self.test_credentials)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["message"], "Login successful")
        self.logger.info("Login success test passed")

    def test_login_wrong_password(self):
        self.logger.debug("Testing login with wrong password")
        response = self.app.post('/login', data={
            "username": "testuser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "login attempt failed.")
        self.logger.info("Wrong password test passed")

    def test_login_user_not_found(self):
        self.logger.debug("Testing login with non-existing user")
        response = self.app.post('/login', data={
            "username": "notexists",
            "password": "whatever"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "login attempt failed.")
        self.logger.info("User not found test passed")

if __name__ == '__main__':
    unittest.main()
