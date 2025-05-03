from crypto import auth_required
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import socketio
from flask_socketio import join_room
from flask import request
import constants
from ai_service import GeminiAPIWrapperManager, GeminiAPIWrapper
import utils


logger = Logger("socketIO")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()
ai_assistant_dict = GeminiAPIWrapperManager()  # Placeholder for AI assistant instances


@socketio.on("message")
@auth_required
def handle_chat_message(msg):
    username = request.user_info["username"]  # Extract username from the validated token
    user_message = msg.get("text")
    logger.debug(f"Message from user {username}: {user_message}")

    ai_assistant: GeminiAPIWrapper = ai_assistant_dict.get_instance(username)  # Get the AI assistant instance for the user
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
    bot_response = process_message(message=user_message, ai_assistant=ai_assistant, username=username)  # Process the message and get a response
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
    ai_assistant: GeminiAPIWrapper = ai_assistant_dict.get_instance(username)  # Get the AI assistant instance for the user
    join_room(username)  # Add the user to their specific room
    logger.info(f"User {username} joined room '{username}'")
    history = fetch_chat_history(username)
    ai_assistant.start_chat(session_id=username, history=history)  # Start a new chat session with the AI assistant
    logger.info(f"User {username} joined room '{username}'")
    socketio.emit("chat_history", utils.convert_chat_history_to_UI_format(history), to=username)

@socketio.on("disconnect")
@auth_required
def handle_disconnect():
    username = request.user_info["username"]  # Extract username from the validated token
    logger.debug(f"User {username} disconnected")
    ai_assistant: GeminiAPIWrapper = ai_assistant_dict.get_instance(username)
    ai_assistant.end_chat(session_id=username)
    # Optionally, you can save the chat history or perform other cleanup tasks here
    logger.info(f"User {username} ended chat session")

def process_message(message, ai_assistant: GeminiAPIWrapper = None, username=None):
    """
    Process the incoming message and return a response.
    This function can be extended to include more complex logic or API calls.
    """
    bot_response = ai_assistant.send_chat_message(session_id=username, message=message)  # Send the message to the AI assistant
    if bot_response is None:
        logger.error("Error: No response from AI assistant")
        return "Sorry, I couldn't process your request at the moment."
    response_dict = utils.return_json_response_as_dict(utils.clean_bot_response(bot_response))  # Convert the response to a dictionary
    logger.info(f"Response from AI assistant: {response_dict}")
    # process the response dictionary to extract the human-readable response and other details
    human_readable_response = response_dict.get("response")
    category = response_dict.get("category")
    args = response_dict.get("args")
    if category != 'INCOMPLETE':
        # Invoke the GBooking function mapping based on the category of the user request
        pass
    # if category == 'INCOMPLETE' it means more information is needed from the user
    return human_readable_response # Return the response from the AI assistant

def fetch_chat_history(username):
    """
    Fetch the chat history for a given user.
    """
    user_chat_document = db_instance.get_document(collection_name=constants.COLLECTION_CHAT_HISTORY, filter={"username": username})
    if user_chat_document:
        history = user_chat_document["messages"]
        return history
    else:
        return []  # Return an empty list if no chat history is found
