from flask import Flask
from flask_basicauth import BasicAuth

app = Flask(__name__)

# Configure basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'yourusername'
app.config['BASIC_AUTH_PASSWORD'] = 'yourpassword'

basic_auth = BasicAuth(app)

# Protected route
@app.route('/')
@basic_auth.required
def protected_route():
    return "You have access to the protected route!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
