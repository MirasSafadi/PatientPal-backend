<<<<<<< HEAD
from flask_socketio import SocketIO
from gevent import monkey # Import gevent monkey patching
monkey.patch_all()  # Monkey-patch for compatibility

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

=======
from flask import Flask , request , jsonify
from flask_bcrypt import Bcrypt
>>>>>>> 7c12ad9 (register backend)
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
socketio = SocketIO(flask_app, cors_allowed_origins='*', async_mode='gevent')
bcrypt = Bcrypt(flask_app)

<<<<<<< HEAD
import routes, socketIO  # Import routes and socketIO after Flask app initialization
=======
app = Flask(__name__)
logger = Logger("app")
db_instance = MongoDBInterface()
db_instance.connect()
bcrypt = Bcrypt(app)
>>>>>>> 7c12ad9 (register backend)

# Check for debug mode in command-line arguments
debug = False
if '--debug' in sys.argv:
    debug = True
    os.environ["IS_DEBUG"] = "True"
logger.info(f"Debug mode is {'active' if debug else 'inactive'}")

<<<<<<< HEAD
if __name__ == "__main__":
    # Check for debug mode again when running the app
    if '--debug' in sys.argv:
        debug = True
        os.environ["IS_DEBUG"] = "True"
    logger.info(f"Debug mode is {'active' if debug else 'inactive'}")
    socketio.run(flask_app, debug=debug)
=======

@app.route('/')
def hello():
    logger.debug("root enpoint (/) called")
    return '<h1>Hello, World!</h1>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    filter_criteria =  {"username": username }
    if db_instance.get_document("users", filter_criteria): #checking if the user exist
        return jsonify({ "msg": "User already exists" }), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    doc = { "username": username, "password": hashed_pw }
    inserted_id = db_instance.add_document("users", doc)

    return jsonify({ "msg": "User registered", "id": str(inserted_id) }), 201

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 7c12ad9 (register backend)
