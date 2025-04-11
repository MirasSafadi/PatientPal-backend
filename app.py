from flask import Flask
from flask import request, jsonify
import click
from logger import Logger
from dotenv import load_dotenv
from mongodb_interface import MongoDBInterface
import os
import sys
import constants
import settings

# Initialize logger
logger = Logger("app")
logger.debug("Importing settings")

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Check for debug mode in command-line arguments
debug = False
if '--debug' in sys.argv:
    debug = True
    os.environ["IS_DEBUG"] = "True"
logger.info(f"Debug mode is {'active' if debug else 'inactive'}")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()

@app.route('/')
def hello():
    logger.debug("Root endpoint (/) called")
    return '<h1>Hello, World!</h1>'

if __name__ == "__main__":
    # Check for debug mode again when running the app
    if '--debug' in sys.argv:
        debug = True
        os.environ["IS_DEBUG"] = "True"
    logger.info(f"Debug mode is {'active' if debug else 'inactive'}")
    
    # Run the Flask app
    app.run(debug=debug)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.debug("Login endpoint (/login) called")

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        logger.debug(f"Login attempt with username: {username}")

        # חיפוש המשתמש במסד הנתונים
        user = db_instance.get_document("users", {"username": username})

        if user:
            if user.get("password") == password:
                logger.info(f"User '{username}' logged in successfully.")
                return jsonify({"message": "Login successful!"}), 200
            else:
                logger.warning(f"Invalid password for user '{username}'.")
                return jsonify({"message": "Invalid password."}), 401
        else:
            logger.warning(f"User '{username}' not found.")
            return jsonify({"message": "User not found."}), 404

    # GET – החזרת טופס התחברות
    return '''
        <form method="post">
            Username: <input type="text" name="username"/><br/>
            Password: <input type="password" name="password"/><br/>
            <input type="submit" value="Login"/>
        </form>
    '''
