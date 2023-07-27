import logging
import logging.handlers as handlers
import time
import os

log_directory = '/var/log/log_new_orion'
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s -%(message)s')

log_file_path_info = os.path.join(log_directory, 'normal.log')
logHandler = handlers.TimedRotatingFileHandler(log_file_path_info, when='M', interval=1, backupCount=2)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)

log_file_path_error = os.path.join(log_directory, 'error.log')
errorlogHandler = handlers.RotatingFileHandler(log_file_path_error, maxBytes=20, backupCount=2)
errorlogHandler.setLevel(logging.ERROR)
errorlogHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.addHandler(errorlogHandler)

def test():
    while True:
        time.sleep(1)
        logger.info("An INFO Log Statement")
        logger.error("An ERROR Log Statement")

test()