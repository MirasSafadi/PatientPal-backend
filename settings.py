import os
from dotenv import load_dotenv
import constants

load_dotenv()

DB_USERNAME = os.getenv(constants.DB_USERNAME)
DB_PASSWORD = os.getenv(constants.DB_PASSWORD)
IS_DEBUG    = os.getenv(constants.IS_DEBUG, constants.FALSE).lower() == constants.TRUE.lower()
