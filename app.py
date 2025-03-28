from flask import Flask
from logger import Logger
from dotenv import load_dotenv
from mongodb_interface import MongoDBInterface
import os

# Load environment variables from the .env file
load_dotenv()


app = Flask(__name__)
logger = Logger("app")
db_instance = MongoDBInterface()



@app.route('/')
def hello():
    logger.debug("root enpoint (/) called")
    return '<h1>Hello, World!</h1>'
