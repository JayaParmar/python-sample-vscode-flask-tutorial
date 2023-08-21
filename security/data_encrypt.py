# How do I apply this in my web app?
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Generate a random encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    data = request.form.get('data')  # Assuming you're collecting data from a form

    # Encrypt the data
    ciphertext = cipher_suite.encrypt(data.encode())

    return render_template('result.html', result=ciphertext.decode())

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    encrypted_data = request.form.get('encrypted_data')  # From a form

    # Decrypt the data
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())

    return render_template('result.html', result=decrypted_data.decode())

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000, debug=True)
