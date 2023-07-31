from os import environ as env
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import HttpResponseError
import getpass

# Get connection to Azure Portal
key_vault_name="wf-kv"
tenant_id = "87056191-b882-40a4-a668-0b4b65f51e55"
client_id = "921e9af4-a07c-40a8-bd9f-6b414196b508"
client_secret = "N-z8Q~R2Q6rt0Lku0rM9qGNlvMLj9P6VgTBPoc1~"
vault_url = "https://wf-kv.vault.azure.net/"

# Create a ClientSecretCredential instance
credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

# Create a SecretClient instance using the credential
secret_client = SecretClient(vault_url=vault_url, credential=credentials)
try:
    secret_name_username = "ORION-username"
    secret_name_password = "ORION-password"

    # Access stored the Snowflake username and password as secrets in the Key Vault
    SNOWFLAKE_USER_NAME = secret_client.get_secret(secret_name_username).value
    SNOWFLAKE_PASSWORD = secret_client.get_secret(secret_name_password).value
    
except Exception as e:                                                
    print(e)
    print("Cannot connect to vault using fallback")
    SNOWFLAKE_USER_NAME = "ORIONDEVICES"
    SNOWFLAKE_PASSWORD = getpass.getpass("Enter your Snowflake password: ")           

SNOWFLAKE_ACCOUNT =  env.get("SNOWFLAKE_ACCOUNT", "od89048.west-europe.azure")
SNOWFLAKE_DATABASE = env.get("SNOWFLAKE_DATABASE", "TALEND_DB")
SNOWFLAKE_SCHEMA = env.get("SNOWFLAKE_DATABASE", "INFORMATION_SCHEMA")

snowflake_config = {'user':SNOWFLAKE_USER_NAME,'password':SNOWFLAKE_PASSWORD,'account':SNOWFLAKE_ACCOUNT,'database':SNOWFLAKE_DATABASE,'schema':SNOWFLAKE_SCHEMA}

snowflake_config['session_parameters'] = {
    'CLIENT_SESSION_KEEP_ALIVE': True,
    'CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY': 3600  # 1 minute in seconds
    }

#conn = snowflake.connector.connect(**snowflake_config)
#return conn


