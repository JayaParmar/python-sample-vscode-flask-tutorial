from flask import Flask, Response, redirect, request, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import snowflake.connector
import getpass

ctx = snowflake.connector.connect(
    user ='PARMJAY',
    password = getpass.getpass("Enter your Snowflake password: "),
    account = 'od89048.west-europe.azure',
    database = 'TALEND_DB',
    schema = 'INFORMATION_SCHEMA',
    )
cs = ctx.cursor()

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

CORS(app)

@app.route('/queue/read_cust_id_detailed', methods=['GET'])
def customer_id_detailed():
    #customer_id_queue = request.args.get('customer_id')    
    customer_id_queue = input("Enter customer Id: ")                                 
    cs.execute('SELECT "Name", "SerialNumber", "iv_Equipment_Type__c", "ExtractionDate", "iv_Equipment_Registration__c" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "Name" = customer_id_queue', {"customer_id_queue": customer_id_queue}) # "alerts" - to be added
    rows = cs.fetchall() 
    cust_device_dict = [{"name": row[0], "DeviceId": row[1], "DeviceType": row[2], "LastActivityTimestamp": row[3], "machineState":row[4]} for row in rows]
    return jsonify({'customer_id_detailed.html': cust_device_dict}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8880, host='0.0.0.0')

cs.close()
ctx.close()