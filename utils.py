from math import log
import constants, jwt, settings, json
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
from logger import Logger
from itsdangerous import URLSafeTimedSerializer
import settings
from flask import jsonify,url_for
import re




logger = Logger("utils")


def convert_ts_to_datetime(ts: str):
    """
        Convert a timestamp to a datetime object.
        The timestamp should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    """
    if ts is None or ts == "":
        return None
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")

def convert_datetime_to_ts(dt: datetime):
    """
        Convert a datetime object to a timestamp.
        The timestamp will be in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    """
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_utc_now_plus_24_hours():
    utc_now = datetime.now(timezone.utc) # Get current UTC time
    new_utc_time = utc_now + timedelta(days=1) # Add 24 hours (1 day)
    unix_timestamp = int(new_utc_time.timestamp()) # Convert the new UTC time to Unix timestamp
    return unix_timestamp


s = URLSafeTimedSerializer(settings.CONFIRM_SECRET_KEY)
# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email)

# Strong password validation
def is_strong_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
    return re.match(pattern, password)

def is_valid_israeli_phone(number):
    pattern = r'^(\+972|972|0)?(5[0-9]|[2-4,8,9][0-9])[-]?[0-9]{7}$'
    return re.fullmatch(pattern, number) is not None
def validation(username, email, password, confirm_password):
    # Validate required
    if not all([username, email, password, confirm_password]):
        return jsonify({ "error": "Username, email, and passwords are required." }), 400
    
    if not is_valid_email(email):
        return jsonify({ "error": "Invalid email format." }), 400
   
    if not is_strong_password(password):
        return jsonify({ "error": "Password must be 8+ chars, 1 uppercase, 1 number." }), 400
   
    if password != confirm_password:
        return jsonify({ "error": "Passwords do not match." }), 400

def generate_registration_token(user):
    return s.dumps(user, salt='register-confirm')

def confirm_token(token):
    try:
        data = s.loads(token, salt='register-confirm', max_age=3600)  # token expiration in seconds (1 hour)
    except:
        return False
    return data

def convert_chat_history_to_UI_format(history):
    if history:
        return [{"sender": "user" if msg["role"] == "user" else "server", "text": " ".join(msg["parts"])} for msg in history]
    else:
        return []
    
def clean_bot_response(response):
    """
        Clean the bot response by removing unwanted characters and formatting.
        This function should be called before sending the response to the user.
    """
    if response is None:
        return None
    logger.debug(f"Raw response: {response}")
    response = response.replace(r"```json", "") # Remove JSON format specifier
    response = response.replace(r"```", "") # Remove triple quotes
    # Remove unwanted characters and format the response
    # response = re.sub(r'\n+', '\n', response)  # Remove extra newlines
    # cleaned_response = re.sub(r'\s+', ' ', response).strip()
    logger.debug(f"Cleaned response: {response}")
    return response

def return_json_response_as_dict(response):
    """
        Convert the JSON response to a dictionary.
        This function should be called after receiving the response from the bot.
    """
    if response is None:
        return None
    try:
        response_dict = json.loads(response)
        return response_dict
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None

