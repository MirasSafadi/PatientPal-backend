from flask import Flask , request , jsonify
from crypto import auth_required, generate_token
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import flask_app, bcrypt
import os, re, utils, settings, smtplib
from email.message import EmailMessage

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()
logger = Logger("routes")


@flask_app.route('/')
def hello():
    logger.debug("Root endpoint (/) called")
    return '<h1>Hello, World!</h1>'

@flask_app.route('/ping')
@auth_required
def ping():
    logger.debug("Ping endpoint (/ping) called")
    return '<h1>Pong</h1>'

@flask_app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    id_number=data.get('id_number')

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
@flask_app.route('/confirm/<token>')
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

@flask_app.route('/login', methods=['POST'])
def login():
    logger.debug("Login endpoint (/login) called")

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None:
            return jsonify({"error": "bad request"}), 400

        logger.debug(f"Login attempt with username: {username}")

        # חיפוש המשתמש במסד הנתונים
        user = db_instance.get_document("users", {"username": username})

        if user is not None:
            if bcrypt.check_password_hash(pw_hash=user.get("password"), password=password):
                logger.info(f"User '{username}' logged in successfully.")
                token = generate_token({"username": username, "hashed_password": user.get("password")})
                
                # 🔒 hash the token and save in db
                hashed_token = bcrypt.generate_password_hash(token).decode('utf-8')
                db_instance.update_document("users", {"username": username}, {"session_token": hashed_token})

                return jsonify({"message": "Login successful", "token": token}), 200

        logger.warning(f"User '{username}' login attempt failed.")
        return jsonify({"message": "login attempt failed."}), 404

    return jsonify({"error": "Wrong method"}), 405
