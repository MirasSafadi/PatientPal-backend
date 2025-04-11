"""
Here will be the crypto module for the project.
This module will contain the functions for encrypting and decrypting data.
"""
from functools import wraps
from flask import jsonify, request
from flask_socketio import emit
import jwt, settings, utils
from datetime import datetime, timedelta, timezone
from logger import Logger
from mongodb_interface import MongoDBInterface
from app import bcrypt,flask_app,socketio

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
        username = request.headers.get("Username") # Username: <username>

        if username is None or token is None:
            if is_socketio:
                emit('error', {"error": "Unauthorized"}, broadcast=False)
                return
            else:
                return jsonify({"error": "Unauthorized"}), 401
        
        #validate the token
        if not validate_token(token):
            if is_socketio:
                emit('error', {"error": "Invalid or expired token"}, broadcast=False)
                return
            else:
                return jsonify({"error": "Invalid or expired token"}), 498
        token = token.split(" ")[1]  # Extract the token from the "Bearer <token>" format

        # Fetch user from the database
        user = db_instance.get_document("users", {"username": username})
        if user is None:
            if is_socketio:
                emit('error', {"error": "Not Found: No such user"}, broadcast=False)
                return
            else:
                return jsonify({"error": "Not Found: No such user"}), 404

        # Compare the token with the stored hashed token
        if not bcrypt.check_password_hash(pw_hash=user.get("hashed_token"), password=token):
            if is_socketio:
                emit('error', {"error": "Unauthorized"}, broadcast=False)
                return
            else:
                logger.debug("Token does not match the stored hashed token")
                return jsonify({"error": "Unauthorized"}), 401
        # If authentication passes, proceed to the endpoint
        return func(*args, **kwargs)
    return wrapper

def validate_token(token: str):
    """
        Validate the token by checking if it is a valid JWT token.
        This function should be called before every endpoint that requires authentication.
        Authorization: Bearer <token>
    """
    if token is None or token == "" or "Bearer" not in token:
        return False
    # Decode the token and check if it is valid
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
        # check password again
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def generate_token(payload: dict):
    """
        Generate a JWT token for the user.
        The token will be valid for 24 hours.
    """
    if payload is None:
        return None
    # Set the expiration time for the token (24 hours)
    expiration = utils.get_utc_now_plus_24_hours()
    # Add the expiration time to the payload
    payload['exp'] = expiration
    token = jwt.encode(payload, settings.JWT_SECRET)
    return token