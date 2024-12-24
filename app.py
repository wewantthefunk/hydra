from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import crypto_asymmetric, crypto_symmetric, utilities
import base64, sqlite3
from datetime import datetime

PRIVATE_KEY = None

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/landing")
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def login():
    global PRIVATE_KEY
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'username': data.get('field1'),
            'password': data.get('field2'),
            'tempPassword': data.get('field3')
        }

        byte_array = base64.b64decode(processed_data['tempPassword'])
        tempPassword = crypto_asymmetric.rsa_decrypt(private_key=PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['username'])
        uname = crypto_asymmetric.rsa_decrypt(private_key=PRIVATE_KEY, encrypted_message=byte_array)

        conn = sqlite3.connect('data/user_db.db')

        # Create a cursor object
        CURSOR = conn.cursor()

        # Retrieve all users
        CURSOR.execute("SELECT * FROM users where username = '" + uname + "'")

        # Fetch all the rows
        rows = CURSOR.fetchall()

        if len(rows) < 1:
            return jsonify({'error': 'Invalid Username and Password'}), 403
        
        byte_array = base64.b64decode(processed_data['password'])

        password = crypto_asymmetric.rsa_decrypt(private_key=PRIVATE_KEY, encrypted_message=byte_array)

        passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0][2]) , password.encode('utf-8'))

        if passphrase == 'valid password: ' + uname:
            token = utilities.generate_random_string(15)
            jdate = utilities.date_to_julian(datetime.now())
            CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate) + " OR username = '" + uname + "'")
            conn.commit()
            CURSOR.execute("INSERT INTO session (token, username, issued) VALUES ('" + token + "','" + uname + "'," + str(jdate) + ")")
            conn.commit()
            tp = base64.b64encode(crypto_symmetric.encrypt(token, tempPassword.encode('utf-8'))).decode('ascii')
            return jsonify({'message': 'success', 'token': tp}), 200
        else:
            return jsonify({'error': 'Invalid Username and Password'}), 403
    else:
        return jsonify({'error': 'Invalid Request'}), 400

@app.route("/check", methods=['POST'])
def checkToken():
    global PRIVATE_KEY
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'token': data.get('field1'),
            'username': data.get('field2')
        }

        byte_array = base64.b64decode(processed_data['token'])
        token = crypto_asymmetric.rsa_decrypt(private_key=PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['username'])
        uname = crypto_asymmetric.rsa_decrypt(private_key=PRIVATE_KEY, encrypted_message=byte_array)

        jdate = utilities.date_to_julian(datetime.now())

        conn = sqlite3.connect('data/user_db.db')

        # Create a cursor object
        CURSOR = conn.cursor()

        CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate))
        conn.commit()

        # Retrieve all users
        CURSOR.execute("SELECT * FROM session WHERE username = '" + uname + "' AND token = '" + token + "' AND issued = " + str(jdate))
        rows = CURSOR.fetchall()

        if len(rows) < 1:
            return jsonify({'error': 'Invalid Token'}), 403
        
        return jsonify({'message': 'success'}), 200

def load_private_key():
    global PRIVATE_KEY
    with open("private/private.pem", "rb") as f:
        PRIVATE_KEY = serialization.load_pem_private_key(
            f.read(),
            password=None,  # If the key is encrypted, provide the password here. Otherwise, use `None`.
            backend=default_backend()
        )


if __name__ == '__main__':
    load_private_key()
    app.run(debug=True)