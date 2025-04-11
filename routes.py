from crypto import auth_required
from mongodb_interface import MongoDBInterface
from logger import Logger
from app import flask_app

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