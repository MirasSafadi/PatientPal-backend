"""
Here will be the crypto module for the project.
This module will contain the functions for encrypting and decrypting data.
"""
from functools import wraps
from flask import jsonify, request
from flask_socketio import emit, disconnect
import jwt, settings, utils
from logger import Logger
from mongodb_interface import MongoDBInterface
from app import bcrypt

logger = Logger("crypto")
db_instance = MongoDBInterface()
db_instance.connect()


def auth_required(func):
    """
        Decorator to validate the authentication token for an endpoint.
        Validate the authentication token by comparing the JWT token in the database 
        with the one in the request. return True if the token is valid, otherwise return False.
        Token saved in the database is a hashed token and should be rotated every 24 hours.
        This function is should be called before every endpoint that requires authentication.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_socketio = hasattr(request, 'sid') # Check if the request is from SocketIO
        token = request.headers.get("Authorization") # Authorization: Bearer <token>

        # Validate the token
        payload, isValid = validate_token(token)
        if not isValid or payload is None:
            # Token is invalid or expired
            logger.debug("Token is invalid or expired")
            if is_socketio:
                emit('error', {"error": "Invalid or expired token"}, broadcast=False)
                disconnect()
                return
            else:
                return jsonify({"error": "Invalid or expired token"}), 498
        token = token.split(" ")[1]  # Extract the token from the "Bearer <token>" format
        username = payload.get("username") # Extract the username from the payload
            
        # Fetch user from the database
        user = db_instance.get_document("users", {"username": username})
        if user is None:
            logger.debug("User not found in the database")
            if is_socketio:
                emit('error', {"error": "Not Found: No such user"}, broadcast=False)
                disconnect()
                return
            else:
                return jsonify({"error": "Not Found: No such user"}), 404

        # Compare the token with the stored hashed token
        if not bcrypt.check_password_hash(pw_hash=user.get("hashed_token"), password=token):
            logger.debug("Token does not match the stored hashed token")
            if is_socketio:
                emit('error', {"error": "Unauthorized"}, broadcast=False)
                disconnect()
                return
            else:
                logger.debug("Token does not match the stored hashed token")
                return jsonify({"error": "Unauthorized"}), 401
        # If authentication passes, proceed to the endpoint
        request.user_info = {"username": username} # Store user info in request for later use in socketio events
        logger.debug(f"User {username} authenticated successfully.")
        return func(*args, **kwargs)
    return wrapper

def validate_token(token: str):
    """
        Validate the token by checking if it is a valid JWT token.
        This function should be called before every endpoint that requires authentication.
        Authorization: Bearer <token>
        Returns (payload, isValid): Payload, and True if the token is valid, otherwise False. 
    """
    if token is None or token == "" or not token.startswith("Bearer "):
        return None, False
    token = token.split(" ")[1]  # Extract the token from the "Bearer <token>" format
    # Decode the token and check if it is valid
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        # check password again
        username = payload.get("username")
        hashed_password = payload.get("hashed_password")
        logger.debug(f"Validating token for user: {username}.")
        user_document = db_instance.get_document("users", {"username": username})

        predicates = [username is None, 
                      username == "",
                      hashed_password is None, 
                      hashed_password == "",
                      user_document is None,
                      bcrypt.check_password_hash(pw_hash=user_document.get("password"), password=hashed_password)
                      ]
        if any(predicates):
            logger.debug("Token validation failed")
            return None, False
        return payload, True
    except jwt.ExpiredSignatureError as e:
        logger.debug("Expired token detected")
        logger.error(e)
        return None, False
    except jwt.InvalidTokenError as e:
        logger.debug("Invalid token detected")
        logger.error(e)
        return None, False

def generate_token(payload: dict):
    """
        Generate a JWT token for the user.
        The token will be valid for 24 hours.
        payload should contain the username and hashed password.
        The token will be used to authenticate the user.
        This function should be called when a user successfully logs in.
    """
    if payload is None:
        return None
    # Set the expiration time for the token (24 hours)
    expiration = utils.get_utc_now_plus_24_hours()
    # Add the expiration time to the payload
    payload['exp'] = expiration
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token