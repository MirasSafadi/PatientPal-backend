from crypto import auth_required
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import socketio


logger = Logger("socketIO")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()

@socketio.on("message")
@auth_required
def handle_chat_message(msg):
    logger.debug('Received message from client: ' + msg)
    socketio.send(msg)