from flask_socketio import SocketIO
from gevent import monkey # Import gevent monkey patching
monkey.patch_all()  # Monkey-patch for compatibility

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from logger import Logger
from dotenv import load_dotenv
import os,sys, re, settings, smtplib


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

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def hello():
    logger.debug("root enpoint (/) called")
    return '<h1>Hello, World!</h1>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Optional profile fields
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    phone = data.get('phone', '').strip()
    birthdate = data.get('birthdate', '').strip()
    gender = data.get('gender', '').strip()
    address = data.get('address', '').strip()    
    # Validate required
    utils.validation(username, email, password, confirm_password)
  
    filter_criteria_username =  {"username": username }
    filter_criteria_email =  {"email": email}
    if db_instance.get_document("users", filter_criteria_username) or db_instance.get_document("users", filter_criteria_email) : #checking if the user exist
        return jsonify({ "msg": "User already exists" }), 400

    # Hash password and store
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "username": username,
        "email": email,
        "password": hashed_pw,
        "profile": {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "birthdate": birthdate,
            "gender": gender,
            "address": address
        }
    }


    token = utils.generate_registration_token(user)
        
# Create the email
    msg = EmailMessage()
    msg['Subject'] = 'Confirm your account'
    msg['From'] = settings.MAIL_USERNAME
    msg['To'] = user['email']
    msg.set_content(f'Hi there!\n\nThank you for signing up. Please confirm your email by clicking the link below:\n\n{request.host_url}/confirm/{token}')
# Send the ema
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME,settings.MAIL_PASSWORD)
        server.send_message(msg)



    #inserted_id = db_interface.add_document("users", user)

    #return jsonify({ "msg": "User registered", "id": str(inserted_id) }), 201
    return  jsonify({
        'message': 'A confirmation email has been sent. Please confirm your registration.',
        'code': 200,
    }), 200
@app.route('/confirm/<token>')
def confirm_registration(token):
    data = utils.confirm_token(token)
    if not data:
        return jsonify({'message': 'The confirmation link is invalid or has expired.', 'code': 400}), 400
    user = {
        "username": data['username'],
        "email": data['email'],
        "password": data['password'],
        "profile": {
            "first_name": data['profile']['first_name'],
            "last_name": data['profile']['last_name'],
            "phone": data['profile']['phone'],
            "birthdate": data['profile']['birthdate'],
            "gender": data['profile']['gender'],
            "address": data['profile']['address']
        }
    }
     # Check if user already exists
    filter_criteria_username =  {"username": user['username'] }
    filter_criteria_email =  {"email": user['email']}
    if db_instance.get_document("users", filter_criteria_username) or db_instance.get_document("users", filter_criteria_email) : #checking if the user exist
        return jsonify({ "msg": "User already exists" }), 400


    # Create new user
    inserted_id = db_instance.add_document("users", user)
    return jsonify({ "msg": "User registered", "id": str(inserted_id) }), 201
