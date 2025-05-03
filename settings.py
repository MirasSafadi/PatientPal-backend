import os
from dotenv import load_dotenv
import constants

load_dotenv()
CONFIRM_SECRET_KEY  = os.getenv(constants.CONFIRM_SECRET_KEY)
MAIL_USERNAME       = os.getenv(constants.MAIL_USERNAME)
MAIL_PASSWORD       = os.getenv(constants.MAIL_PASSWORD)
DB_USERNAME         = os.getenv(constants.DB_USERNAME)
DB_PASSWORD         = os.getenv(constants.DB_PASSWORD)
JWT_SECRET          = os.getenv(constants.JWT_SECRET)
IS_DEBUG            = os.getenv(constants.IS_DEBUG, constants.FALSE).lower() == constants.TRUE.lower()
GEMINI_API_KEY      = os.getenv(constants.GEMINI_API_KEY)
GBOOKING_TOKEN      = os.getenv(constants.GBOOKING_TOKEN)
GBOOKING_USER       = os.getenv(constants.GBOOKING_USER)
