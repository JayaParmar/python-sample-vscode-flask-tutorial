from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import database
import logging
import logging.handlers as handlers
import os       

SWAGGER_URL = '/api'
API_URL = '/static/test.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Orion - Customer Dashboard API"
    }
)

app = Flask(__name__)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
engine = database.create_db_connection_pool()

class FlaskLogger:
    def __init__(self, app):
        self.app = app
        self.setup_logger()

    def setup_logger(self):
        log_directory = '/var/log/log_new_orion/'
        os.makedirs(log_directory, exist_ok=True)

        self.app.logger = logging.getLogger('new_orion_app')
        self.app.logger.setLevel(logging.INFO) 

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        log_file_path_info = os.path.join(log_directory, 'normal.log')
        logHandler = handlers.RotatingFileHandler(log_file_path_info, maxBytes=1024*1024, backupCount=5)
        logHandler.setLevel(logging.INFO)
        logHandler.setFormatter(formatter)              
        
        self.app.logger.addHandler(logHandler)        

logger = FlaskLogger(app)

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
    cust_device_dict = database.get_customer_by_id(engine, customer_id)   
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/')
def index():
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    #cust_id = request.args.get('customer-id') 
    #app.logger.info(f'User with IP {client_ip} and User-Agent {user_agent} viewed customer ID {cust_id}')
    app.logger.info(f'User with IP {client_ip} and User-Agent {user_agent}')
    return 'Welcome to the Orion Customer Dashboard API'
    
if __name__ == '__main__':
    app.run(debug=True, port=8444, host='0.0.0.0')                             # This should be https://orion-dev.ivoclarvivadent.com:8444     