from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import getpass

#def get_connection():
TENANT_ID = env.get("AZURE_TENANT_ID", "")
CLIENT_ID = env.get("AZURE_CLIENT_ID", "")
CLIENT_SECRET = env.get("AZURE_CLIENT_SECRET", "")
try:
    KEYVAULT_NAME = env.get("wf-kv", "")
    KEYVAULT_URI = f"https://wf-kv.vault.azure.net/"  
    _credential = ClientSecretCredential(
        tenant_id="87056191-b882-40a4-a668-0b4b65f51e55",                       
        client_id=CLIENT_ID,                                                    # Waiting AAD access. Finding client ID and client Secret (manageengine.com)
        client_secret=CLIENT_SECRET
        )
    _sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
    SNOWFLAKE_USER_NAME = _sc.get_secret("TestSecret").value                 # Change this to the secret username
    SNOWFLAKE_PASSWORD = _sc.get_secret("TestSecretPassword").value
except ValueError as e:                                                
    print(e)
    print("Cannot connect to vault using fallback")
    
    SNOWFLAKE_USER_NAME = env.get("SNOWFLAKE_USER_NAME", "PARMJAY")
    SNOWFLAKE_PASSWORD = env.get("SNOWFLAKE_PASSWORD")                        #set SNOWFLAKE_PASSWORD = your_snowflake_password_here
    if SNOWFLAKE_PASSWORD is None:
        SNOWFLAKE_PASSWORD = getpass.getpass("Enter your Snowflake password: ")           
SNOWFLAKE_ACCOUNT =  env.get("SNOWFLAKE_ACCOUNT", "od89048.west-europe.azure")
SNOWFLAKE_DATABASE = env.get("SNOWFLAKE_DATABASE", "TALEND_DB")
SNOWFLAKE_SCHEMA = env.get("SNOWFLAKE_DATABASE", "INFORMATION_SCHEMA")

snowflake_config = {'user':SNOWFLAKE_USER_NAME,'password':SNOWFLAKE_PASSWORD,'account':SNOWFLAKE_ACCOUNT,'database':SNOWFLAKE_DATABASE,'schema':SNOWFLAKE_SCHEMA}

#snowflake_config['session_parameters'] = {
#    'CLIENT_SESSION_KEEP_ALIVE': True,
#    'CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY': 3600  # 1 minute in seconds
#    }

#conn = snowflake.connector.connect(**snowflake_config)
#return conn
    