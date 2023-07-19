import snowflake.connector
import getpass
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

ctx = snowflake.connector.connect(
    user ='PARMJAY',
    password = getpass.getpass("Enter your Snowflake password: "),
    account = 'od89048.west-europe.azure',
    database = 'TALEND_DB',
    schema = 'INFORMATION_SCHEMA',
    )
cs = ctx.cursor()

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

@app.route('/devices', methods=['GET'])
def customer_id_detailed():
    customer_id = request.args.get('customer-id')      
    device_type = request.args.get('device-type')
    device_ids = request.args.getlist('device-ids')

    query = f"""SELECT "Name", "SerialNumber", "iv_Equipment_Type__c"  FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "Name" = '{customer_id}'"""
    if device_ids:
        query += """ AND "SerialNumber" in '{device_ids}'"""
    if device_type:
        query += """ AND "iv_Equipment_Type__c"  = '{device_type}'"""
    print(query)
    # cs.execute(query, (f"'{customer_id}'", f"'{device_type}'", f"'{device_type}'", f"'{device_ids}'", f"'{device_ids}'"))
    cs.execute(query)

    rows = cs.fetchall() 
    cust_device_dict = [{"name": row[0], "DeviceId": row[1], "DeviceType": row[2]} for row in rows]
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/devices/{device-id}', methods=['GET'])    
def device_id():
    device_id_queue = request.args.get('device-id')                                     
    cs.execute('SELECT "Name", "SerialNumber", "iv_Equipment_Type__c"FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "SerialNumber" = %s', device_id_queue) # "softwareVersion","latitude","longitude","serviceHub","alerts" - database: wf-sandbox-sql (https://collaboration.ivoclarvivadent.com/display/IST/Orion+-+DeviceImporter+for+AzureSQL))
    rows = cs.fetchall() 
    cust_device_dict = [{"name": row[0], "DeviceId": row[1], "DeviceType": row[2]} for row in rows]
    return jsonify({'customer devices': cust_device_dict}), 200

@app.route('/customer', methods=['GET'])
def customer_id_device_id_only():
    customer_id_queue = request.args.get('customer-id')                                     
    cs.execute('SELECT "Name", "SerialNumber" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "Name" = %s', customer_id_queue) 
    rows = cs.fetchall() 
    cust_device_dict = [{"name": row[0], "DeviceId": row[1]} for row in rows]
    return jsonify({'customer devices': cust_device_dict}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8444, host='0.0.0.0')                             # This should be https://orion-dev.ivoclarvivadent.com:8444

cs.close()
ctx.close()


      