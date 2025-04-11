from flask import jsonify, request
from crypto import auth_required, generate_token
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import flask_app,bcrypt

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

@flask_app.route('/login', methods=['POST'])
def login():
    logger.debug("Login endpoint (/login) called")

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username is None or password is None :
            return jsonify({"error": "bad request"}),400
        

        logger.debug(f"Login attempt with username: {username}")

        # חיפוש המשתמש במסד הנתונים
        user = db_instance.get_document("users", {"username": username})

        if user is not None:
            if bcrypt.check_password_hash(pw_hash=user.get("password"), password=password):
                logger.info(f"User '{username}' logged in successfully.")
                token = generate_token({"username": username, "password": user.get("password")})
                # hash the token and save in db
                return jsonify({"message": "Login successful", "token": token}), 200
        logger.warning(f"User '{username}' login attempt failed.")
        return jsonify({"message": "login attempt failed."}), 404
    return jsonify({"error": "Wrong method"}), 405

