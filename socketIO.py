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
    user_message = msg.get("text")
    logger.debug(f"Message from user {username}: {user_message}")
    # Send the message to the user's room
    user_chat_document = db_instance.get_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username})
    if user_chat_document is None:
        # If no chat history exists, create a new document for the user
        db_instance.add_document(collection_name=constants.COLLECTION_CHAT_HISTORY,
                                  document={"username": username, "messages": []})
        # Retrieve the newly created document
        user_chat_document = db_instance.get_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username})
    # If the user has chat history, append the new message to it
    history = user_chat_document["messages"]
    history.append({"role": "user", "parts": [user_message]})
    
    # Process the message and get a response from the bot
    # Here you would typically call your AI service to get a response
    bot_response = process_message(user_message)  # Process the message and get a response
    socketio.emit("message", {"text": bot_response, "sender": "server"}, to=username)

    history.append({"role": "model", "parts": [bot_response]})
    # Update the chat history in the database
    db_instance.update_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username},
                                    update_data={"messages": history})


@socketio.on("connect")
@auth_required
def handle_connect():
    username = request.user_info["username"]  # Extract username from the validated token
    logger.debug(f"User {username} connected")
    join_room(username)  # Add the user to their specific room
    logger.info(f"User {username} joined room '{username}'")
    history = fetch_chat_history(username)
    socketio.emit("chat_history", history, to=username)
    

def process_message(message):
    """
    Process the incoming message and return a response.
    This function can be extended to include more complex logic or API calls.
    """
    # For now, just echo the message back in uppercase
    return message.upper()

def fetch_chat_history(username):
    """
    Fetch the chat history for a given user.
    """
    user_chat_document = db_instance.get_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username})
    if user_chat_document:
        history = user_chat_document["messages"]
        history = [{"sender": "user" if msg["role"] == "user" else "server", "text": " ".join(msg["parts"])} for msg in history]
        return history
    else:
        return []  # Return an empty list if no chat history is found
