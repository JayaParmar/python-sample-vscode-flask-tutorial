from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import database
import logging
import uuid 
import os  
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

SWAGGER_URL = '/api'
API_URL = '/static/test.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Orion - Customer Dashboard API"
    }
)

class FlaskLogger(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(FlaskLogger, self).__init__(logger, extra or {})

    # Not in use
    def process(self, msg, kwargs):
        """
        Add extra information to the log message.
        """
        kwargs["extra"] = self.extra
        return msg, kwargs

app = Flask(__name__)

# Configuration for logging
log_directory = '/var/log/log_new_orion/'
log_file_path_info = os.path.join(log_directory, 'log_app.log')
app.config["LOG_FILE"] = log_file_path_info
app.config["LOG_LEVEL"] = logging.INFO

def setup_logger():
    logger = logging.getLogger("new_orion_app")
    logger.setLevel(app.config["LOG_LEVEL"])
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(request_id)s] - [%(user_ip)s] - [%(cust_id)s] - %(message)s"
    )
    
    # Creates daily log file at midnight with backup logs for last 7 days 
    timed_handler = TimedRotatingFileHandler(app.config["LOG_FILE"], when='midnight', backupCount=7)      
    timed_handler.setLevel(app.config["LOG_LEVEL"])
    timed_handler.setFormatter(formatter)
    logger.addHandler(timed_handler)

    # Rotating when the log file reaches 50 MB and keeping at most 3 backup files
    rotating_handler = RotatingFileHandler(app.config["LOG_FILE"], maxBytes=50 * 1024 * 1024, backupCount=3)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)

    return logger

# Create an instance of FlaskLogger using the setup logger
flask_logger = FlaskLogger(setup_logger(), extra={"user_ip": "", "request_id": "","cust_id": ""})

@app.before_request
def before_request():
    # Generate a unique request_id, user_ip and cust_id to the FlaskLogger extra.
    flask_logger.extra["request_id"] = str(uuid.uuid4())

    # Get the user IP address from the request
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    flask_logger.extra["user_ip"] = user_ip

    # Get the cust_id from the request
    cust_id = request.args.get("customer-id")
    flask_logger.extra["cust_id"] = cust_id 
 
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
engine = database.create_db_connection_pool()

# Error handler to catch exceptions and log them with the appropriate log level
@app.errorhandler(Exception)
def handle_error(error):
    flask_logger.exception("An unhandled exception occurred.")
    flask_logger.critical("CRITICAL: A critical error occurred!")
    return "An unexpected error occurred.", 500

@app.route('/devices', methods=['GET'])
def customer_id_detailed():
    customer_id = request.args.get('customer-id')      
    device_type = request.args.get('device-type')
    device_ids = request.args.getlist('device-ids')
    cust_device_dict = database.get_customer_devices(engine, customer_id, device_type, device_ids)
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/devices/{device-id}', methods=['GET'])    
def device_id():
    device_id = request.args.get('device-id')                                     
    cust_device_dict = database.get_device_by_id(engine, device_id)    
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/customer', methods=['GET'])
def customer_id_device_id_only():
    customer_id = request.args.get('customer-id')  
    flask_logger.info(f'User access the customer id')      
    cust_device_dict = database.get_customer_by_id(engine, customer_id)   
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/')
def index():    
    flask_logger.info(f'User access the index page')    
    return 'Welcome to the Orion Customer Dashboard API'
    
if __name__ == '__main__':
    app.run(debug=True, port=8444, host='0.0.0.0')                             # This should be https://orion-dev.ivoclarvivadent.com:8444     






