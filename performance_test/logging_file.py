import logging
import logging.handlers as handlers
import time

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

## Here we define our formatter i.e. specify the layout of log records in the final output.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Handlers send the log records (created by loggers) to the appropriate destination.
logHandler = handlers.TimedRotatingFileHandler('timed_app.log', when='M', interval=1, backupCount=2)
logHandler.setLevel(logging.INFO)

## Here we set our logHandler's formatter
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

def main():
    while True:
        time.sleep(100)
        logger.info("A Sample Log Statement")

main()






# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')