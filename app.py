from flask_socketio import SocketIO
from gevent import monkey # Import gevent monkey patching
monkey.patch_all()  # Monkey-patch for compatibility

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from logger import Logger
from dotenv import load_dotenv
import os,sys


# Initialize logger
logger = Logger("app")
logger.debug("Importing settings")

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
flask_app = Flask(__name__)
CORS(flask_app)  # Enable CORS for all routes
socketio = SocketIO(flask_app, cors_allowed_origins='*')
bcrypt = Bcrypt(flask_app)

import routes, socketIO  # Import routes and socketIO after Flask app initialization

# Check for debug mode in command-line arguments
debug = False
if '--debug' in sys.argv:
    debug = True
    os.environ["IS_DEBUG"] = "True"
logger.info(f"Debug mode is {'active' if debug else 'inactive'}")

if __name__ == "__main__":
    # Check for debug mode again when running the app
    if '--debug' in sys.argv:
        debug = True
        os.environ["IS_DEBUG"] = "True"
    logger.info(f"Debug mode is {'active' if debug else 'inactive'}")
    socketio.run(flask_app, debug=debug)