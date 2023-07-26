from flask import Flask, jsonify, request
from os import environ as env
import getpass
from sqlalchemy import create_engine, text
from flask_swagger_ui import get_swaggerui_blueprint

# Database credentials
SNOWFLAKE_USER_NAME = env.get("SNOWFLAKE_USER_NAME", "PARMJAY")
SNOWFLAKE_PASSWORD = getpass.getpass("Enter your Snowflake password: ")           
SNOWFLAKE_ACCOUNT =  env.get("SNOWFLAKE_ACCOUNT", "od89048.west-europe.azure")
SNOWFLAKE_DATABASE = env.get("SNOWFLAKE_DATABASE", "TALEND_DB")
SNOWFLAKE_SCHEMA = env.get("SNOWFLAKE_DATABASE", "INFORMATION_SCHEMA")
snowflake_config = {'user':SNOWFLAKE_USER_NAME,'password':SNOWFLAKE_PASSWORD,'account':SNOWFLAKE_ACCOUNT,'database':SNOWFLAKE_DATABASE,'schema':SNOWFLAKE_SCHEMA}

snowflake_config['session_parameters'] = {
    'CLIENT_SESSION_KEEP_ALIVE': True,
    'CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY': 3600  # 1 minute in seconds
    }

# Make connection
def create_db_connection_pool():
    database_url = f'snowflake://{snowflake_config["user"]}:{snowflake_config["password"]}@{snowflake_config["account"]}/{snowflake_config["database"]}/{snowflake_config["schema"]}'
    engine = create_engine(database_url, pool_size=5, max_overflow=10)
    return engine

SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
API_URL = '/static/api/message_queue.yaml'  # URL where your Swagger YAML file is served

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Message Queuing System API - Line-Up"
    }
)

app = Flask(__name__)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
engine = create_db_connection_pool()

@app.route('/queue/create', methods=['POST'])
def create_queue():
    queue_name = request.json.get('name')
    f"""INSERT INTO queues (name, messages) VALUES (?, ?), (queue_name, '[]'))"""
    return jsonify({'message': f'Queue "{queue_name}" created.'}), 201

@app.route('/devices/{device-id}', methods=['GET'])    
def device_id():
    device_id = request.args.get('device-id') 
    #query = f"""SELECT "iv_External_Id__c", "SerialNumber", "iv_Equipment_Type__c" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "SerialNumber" = '{device_id}'"""
    
    # Get a connection from the engine
    with engine.connect() as conn:
    # SQL statement using Connection.execute()
        result = conn.execute(f"""SELECT "iv_External_Id__c", "SerialNumber", "iv_Equipment_Type__c" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "SerialNumber" = '{device_id}'""")
        rows = result.fetchall()
        cust_device_dict = [{"iv_External_Id__c": row[0], "DeviceId": row[1], "DeviceType": row[2]} for row in rows]
        return jsonify({'customer devices': cust_device_dict}), 200       
    
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
