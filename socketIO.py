from crypto import auth_required
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import socketio
from flask_socketio import join_room
from flask import request
import constants



logger = Logger("socketIO")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()

@socketio.on("message")
@auth_required
def handle_chat_message(msg):
    username = request.user_info["username"]  # Extract username from the validated token
    message = msg.get("text")
    logger.debug(f"Message from user {username}: {message}")
    # Send the message to the user's room
    user_chat_documents = db_instance.get_documents(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username})
    if user_chat_documents:
        # If the user has chat history, append the new message to it
        user_chat_documents[0]["messages"].append({"role": "user", "parts": [message]})
        db_instance.update_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username}, update={"$set": {"messages": user_chat_documents[0]["messages"]}})
    else:
        # If no chat history exists, create a new document for the user
        db_instance.create_document(collection_name=constants.COLLECTION_CHAT_HISTORY, document={"username": username, "messages": [{"role": "user", "parts": [message]}]})
    bot_response = process_message(message)  # Process the message and get a response
    socketio.emit("message", {"text": bot_response, "sender": "server"}, to=username)
    # Add the bot's response to the user's chat history
    if user_chat_documents:
        # If the user has chat history, append the bot's response to it
        user_chat_documents[0]["messages"].append({"role": "model", "parts": [bot_response]})
        db_instance.update_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username}, update={"$set": {"messages": user_chat_documents[0]["messages"]}})
    else:
        # If no chat history exists, create a new document for the user with the bot's response
        db_instance.create_document(collection_name=constants.COLLECTION_CHAT_HISTORY, document={"username": username, "messages": [{"role": "model", "parts": [bot_response]}]})

@socketio.on("connect")
@auth_required
def handle_connect():
    username = request.user_info["username"]  # Extract username from the validated token
    logger.debug(f"User {username} connected")
    join_room(username)  # Add the user to their specific room
    logger.info(f"User {username} joined room '{username}'")

def process_message(message):
    """
    Process the incoming message and return a response.
    This function can be extended to include more complex logic or API calls.
    """
    # For now, just echo the message back in uppercase
    return message.upper()