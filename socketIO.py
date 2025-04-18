from math import log
from crypto import auth_required
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import socketio
from flask_socketio import emit, join_room
from flask import request


logger = Logger("socketIO")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()

@socketio.on("message")
@auth_required
def handle_chat_message(msg):
    username = request.user_info["username"]  # Extract username from the validated token
    message = msg.get("text")
    logger.info(f"Message from user {username}: {message}")
    # Send the message to the user's room
    # socketio.emit("message", {"text": message.upper(), "sender": "server"})
    socketio.emit("message", {"text": message.upper(), "sender": "server"}, to=username)

@socketio.on("connect")
@auth_required
def handle_connect():
    username = request.user_info["username"]  # Extract username from the validated token
    logger.info(f"User {username} connected")
    join_room(username)  # Add the user to their specific room
    logger.info(f"User {username} joined room '{username}'")