from sqlalchemy import create_engine
import config
import signal,sys

def create_db_connection_pool():
    database_url = f'snowflake://{config.snowflake_config["user"]}:{config.snowflake_config["password"]}@{config.snowflake_config["account"]}/{config.snowflake_config["database"]}/{config.snowflake_config["schema"]}'
    engine = create_engine(database_url, pool_size=30, max_overflow=10)    # pool_size = active connections to database to handle incoming requests
    # engine = enginemaker(bind=engine)
    return engine

def get_customer_devices(engine, customer_id, device_type, device_ids):
    query = f"""SELECT "iv_External_Id__c", "SerialNumber", "iv_Equipment_Type__c"  FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "iv_External_Id__c" = '{customer_id}'"""
    
    if device_ids:
        query += f""" AND "SerialNumber" in ('{"','".join(device_ids)}')"""
    
    if device_type:
        query += f""" AND "iv_Equipment_Type__c"  = '{device_type}'"""
    
    result = engine.execute(query)
    rows = result.fetchall()
    cust_device_dict = [{"iv_External_Id__c": row[0], "DeviceId": row[1], "DeviceType": row[2]} for row in rows]
    return cust_device_dict

def get_device_by_id(engine, device_id):
    query = f"""SELECT "iv_External_Id__c", "SerialNumber", "iv_Equipment_Type__c" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "SerialNumber" = '{device_id}'"""
    result = engine.execute(query)
    rows = result.fetchall()
    cust_device_dict = [{"iv_External_Id__c": row[0], "DeviceId": row[1], "DeviceType": row[2]} for row in rows]
    return cust_device_dict

def get_customer_by_id(engine, customer_id):
    query = f"""SELECT "iv_External_Id__c", "SerialNumber" FROM TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET WHERE "iv_External_Id__c" = '{customer_id}'"""
    result = engine.execute(query)
    rows = result.fetchall()
    cust_device_dict = [{"iv_External_Id__c": row[0], "DeviceId": row[1]} for row in rows]
    return cust_device_dict

def graceful_shutdown(signum, frame):
    print("Received SIGINT. Gracefully shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)
