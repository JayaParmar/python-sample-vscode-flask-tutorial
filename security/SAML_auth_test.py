from flask import Flask, request, redirect
from onelogin.saml2.auth import OneLogin_Saml2_Auth

app = Flask(__name__)

# SAML configuration settings
SAML_SETTINGS = {
    'strict': True,
    'debug': False,
    'sp': {
        'entityId': 'your_sp_entity_id',               # this is the client secret from MS Azure app registration
        'assertionConsumerService': {
            'url': 'http://localhost:5000/sso/acs',
            'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
        },
        # Add more SP settings as needed
    },
    'idp': {
        'entityId': 'your_idp_entity_id',            # client email
        'singleSignOnService': {
            'url': 'https://idp.example.com/sso',
            'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
        },
        # Add more IdP settings as needed
    },
}

@app.route('/login')
def login():
    auth = OneLogin_Saml2_Auth(request.environ, SAML_SETTINGS)
    return redirect(auth.login())

@app.route('/sso/acs', methods=['POST'])
def acs():
    auth = OneLogin_Saml2_Auth(request.environ, SAML_SETTINGS)
    auth.process_response()
    if auth.is_authenticated():
        # User is authenticated
        user_data = auth.get_attributes()
        return f"Welcome, {user_data.get('email')[0]}!"
    else:
        return "Authentication failed."

if __name__ == '__main__':
    app.run(debug=True)
