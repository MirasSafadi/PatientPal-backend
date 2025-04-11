import constants, jwt, settings
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