from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import database

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

if __name__ == '__main__':
    app.run(debug=True, port=8444, host='0.0.0.0')                             # This should be https://orion-dev.ivoclarvivadent.com:8444




      