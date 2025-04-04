from flask import Flask
import click
from logger import Logger
from dotenv import load_dotenv
from mongodb_interface import MongoDBInterface
import os
import sys
import constants
import settings

# Initialize logger
logger = Logger("app")
logger.debug("Importing settings")

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Check for debug mode in command-line arguments
debug = False
if '--debug' in sys.argv:
    debug = True
    os.environ["IS_DEBUG"] = "True"
logger.info(f"Debug mode is {'active' if debug else 'inactive'}")

# Initialize database connection
db_instance = MongoDBInterface()
db_instance.connect()

@app.route('/')
def hello():
    logger.debug("Root endpoint (/) called")
    return '<h1>Hello, World!</h1>'

if __name__ == "__main__":
    # Check for debug mode again when running the app
    if '--debug' in sys.argv:
        debug = True
        os.environ["IS_DEBUG"] = "True"
    logger.info(f"Debug mode is {'active' if debug else 'inactive'}")
    
    # Run the Flask app
    app.run(debug=debug)