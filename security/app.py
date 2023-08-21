from flask import Flask
from OpenSSL import SSL

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8444, debug=True, ssl_context=('server-signed-cert1.pem', 'server-key.pem'))
    