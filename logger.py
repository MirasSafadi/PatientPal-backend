import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self,module):
        self.module = module
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.DEBUG)
        self.__initialize()
        

    def __initialize(self):
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # initialize rotating file handler
        rotating_file_handler = RotatingFileHandler(f'logs/{self.module}.log', maxBytes=2000, backupCount=3) # logs to a file
        rotating_file_handler.setFormatter(format)
        rotating_file_handler.setLevel(logging.DEBUG)
        # initialize console handler
        console_handler = logging.StreamHandler() # logs to the console
        console_handler.setFormatter(format)
        console_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(rotating_file_handler)
        #Supress debug logs of 3rd party libraries
        logging.getLogger("requests").setLevel(logging.WARN)
        logging.getLogger("pymongo").setLevel(logging.WARN)
        logging.getLogger("flask").setLevel(logging.WARN)
        
    def info(self,message):
        self.logger.info(message)

    def debug(self,message):
        self.logger.debug(message)

    def warning(self,message):
        self.logger.warning(message)

    def error(self,message):
        self.logger.error(message)

    def critical(self,message):
        self.logger.critical(message)

"""
Example usage (in another file):
logger = Logger("app")

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

app.log:
2025-03-28 18:36:45,051 - app - DEBUG - This is a debug message
2025-03-28 18:36:45,051 - app - INFO - This is an info message
2025-03-28 18:36:45,051 - app - WARNING - This is a warning message
2025-03-28 18:36:45,051 - app - ERROR - This is an error message
2025-03-28 18:36:45,051 - app - CRITICAL - This is a critical message
"""