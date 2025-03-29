from flask import Flask , request , jsonify
from flask_bcrypt import Bcrypt
from logger import Logger
from dotenv import load_dotenv
from mongodb_interface import MongoDBInterface
import os

# Load environment variables from the .env file
load_dotenv()


app = Flask(__name__)
logger = Logger("app")
db_instance = MongoDBInterface()
db_instance.connect()
bcrypt = Bcrypt(app)



@app.route('/')
def hello():
    logger.debug("root enpoint (/) called")
    return '<h1>Hello, World!</h1>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    filter_criteria =  {"username": username }
    if db_instance.get_document("users", filter_criteria): #checking if the user exist
        return jsonify({ "msg": "User already exists" }), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    doc = { "username": username, "password": hashed_pw }
    inserted_id = db_instance.add_document("users", doc)

    return jsonify({ "msg": "User registered", "id": str(inserted_id) }), 201

if __name__ == "__main__":
    app.run(debug=True)
