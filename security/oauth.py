from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

oauth = OAuth(app)

# Configure OAuth provider
oauth_providers = {
    'example': {
        'client_id': 'your_client_id',
        'client_secret': 'your_client_secret',
        'authorize_url': 'https://example.com/oauth2/authorize',
        'authorize_params': None,
        'access_token_url': 'https://example.com/oauth2/token',
        'access_token_params': None,
        'redirect_uri': 'http://localhost:5000/callback'
    }
}

example = oauth.remote_app(
    'example',
    consumer_key='example',
    request_token_params=None,
    base_url=None,
    request_token_url=None,
    access_token_method='POST',
    access_token_url=None,
    authorize_url='https://example.com/oauth2/authorize'
)

@app.route('/')
def index():
    return 'Welcome to the OAuth example app!'

@app.route('/login')
def login():
    return example.authorize(callback=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    response = example.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    # Store the access token in the session for further use
    session['example_token'] = (response['access_token'], '')
    
    return 'You are now authenticated with OAuth!'

@example.tokengetter
def get_example_oauth_token():
    return session.get('example_token')

if __name__ == '__main__':
    app.run(debug=True)
