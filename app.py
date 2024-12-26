from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import crypto_asymmetric, crypto_symmetric, utilities, constants, businesslogic
import base64, sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('out-index.html', app_name=constants.APP_NAME)

@app.route("/home")
def landing():
    return render_template('in-landing.html', app_name=constants.APP_NAME)

@app.route("/newuser")
def newuser():
    return render_template('out-newuser.html', app_name=constants.APP_NAME)

@app.route("/verify")
def verify():
    return render_template("out-verify.html", app_name=constants.APP_NAME)

@app.route("/account")
def account():
    return render_template("in-account.html", app_name=constants.APP_NAME)

@app.route("/admin")
def admin():
    return render_template("in-admin.html", app_name=constants.APP_NAME)

@app.route('/getusers', methods=['POST'])
def getusers():
    pass

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'username': data.get('field1'),
            'password': data.get('field2'),
            'tempPassword': data.get('field3')
        }

        result = businesslogic.login(processed_data['username'], processed_data['password'], processed_data['tempPassword'])

        if result['result'] != constants.RESULT_OK:
            return jsonify({'error': result['message']}), result['result']
            
        return jsonify({'message': 'Successful Login', 'token': result['tmp_password'], 'level': result['level']}), constants.RESULT_OK
    else:
        return jsonify({'error': 'Invalid Request'}), constants.RESULT_INVALID_REQUEST

@app.route("/check", methods=['POST'])
def checkToken():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'token': data.get('field1'),
            'username': data.get('field2')
        }

        byte_array = base64.b64decode(processed_data['token'])
        token = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['username'])
        uname = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

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
    
@app.route('/verifyaccount', methods=['POST'])
def verifyaccount():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'code': data.get('field3')
        }

        byte_array = base64.b64decode(processed_data['email'])
        email = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['password'])
        password = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['code'])
        code = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        conn = sqlite3.connect('data/user_db.db')

        # Create a cursor object
        CURSOR = conn.cursor()

        # Retrieve all users
        CURSOR.execute("SELECT * FROM users WHERE email = '" + email + "' AND verificationCode = '" + code + "'")
        rows = CURSOR.fetchall()

        if len(rows) < 1:
            return jsonify({'error': 'Invalid Verification Information'}), 403
        
        passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0][2]) , password.encode('utf-8'))

        if passphrase != 'valid password: ' + rows[0][1]:
            return jsonify({'error': 'Invalid Verification Information'}), 403
        
        CURSOR.execute("UPDATE users SET isVerified = " + str(constants.VERIFIED_ACCOUNT) + " WHERE id = " + str(rows[0][0]))
        conn.commit()

        if str(rows[0][4]) == "0":
            utilities.write_to_file('static/admin_verified.js', "admin_verified=1;")

        return jsonify({'message': 'Verification Successful'}), 200

@app.route('/generateverify', methods=['POST'])
def generateverify():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1')
        }

        byte_array = base64.b64decode(processed_data['email'])
        email = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        conn = sqlite3.connect('data/user_db.db')

        # Create a cursor object
        CURSOR = conn.cursor()

        # Retrieve all users
        CURSOR.execute("SELECT * FROM users  WHERE email = '" + email + "'")
        rows = CURSOR.fetchall()

        if len(rows) < 1:
            return jsonify({'error': 'Email Does Not Exist'}), 400
        
        if rows[0][5] == constants.VERIFIED_ACCOUNT:
            return jsonify({'error': 'Account Already Verified'}), 406
        
        vcode = utilities.generate_random_string(6)

        CURSOR.execute("UPDATE users SET verificationCode = '" + vcode + "' WHERE email = '" + email + "'")
        conn.commit()

        send_verification_email(email, vcode)

        return jsonify({'message': 'Verification Email Sent'}), 200

    return jsonify({'error': 'Invalid Request'}), 400

def load_private_key():
    with open("private/private.pem", "rb") as f:
        constants.PRIVATE_KEY = serialization.load_pem_private_key(
            f.read(),
            password=None,  # If the key is encrypted, provide the password here. Otherwise, use `None`.
            backend=default_backend()
        )

@app.route("/checkadmin")
def checkAdminVerification():
    conn = sqlite3.connect('data/user_db.db')

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE usertype = 0")
    rows = CURSOR.fetchall()

    if len(rows) < 1:
        exit(1000)

    if rows[0][5] == constants.UNVERIFIED_ACCOUNT:
        send_verification_email(rows[0][3], rows[0][6])

    return jsonify({'message': 'success'}), 200 

@app.route("/createaccount", methods=['POST'])
def createaccount():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'username': data.get('field3')
        }

        byte_array = base64.b64decode(processed_data['email'])
        email = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['password'])
        password = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        byte_array = base64.b64decode(processed_data['username'])
        username = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        conn = sqlite3.connect('data/user_db.db')

        # Create a cursor object
        CURSOR = conn.cursor()

        # Retrieve all users
        CURSOR.execute("SELECT * FROM users WHERE email = '" + email + "' OR username = '" + username +  "'")
        rows = CURSOR.fetchall()

        if len(rows) > 0:
            return jsonify({'error': 'Username and/or Email already registered'}), 400
        
        passphrase = 'valid password: ' + username

        p = crypto_symmetric.encrypt(passphrase, password.encode('utf-8'))

        vcode = utilities.generate_random_string(6)

        CURSOR.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive) VALUES ('" + username + "', '" + base64.b64encode(p).decode('ascii') + "','" + email + "', 99, 0,'" + vcode + "',1)")
        conn.commit()

        send_verification_email(email, vcode)

        return jsonify({'message': 'Account Creation Successful! You must verify your account before you can login!'}), 200

def send_verification_email(email: str, code: str):
    hostJson = utilities.load_json_file('private/url.json')
    url = hostJson['url']

    portJson = utilities.load_json_file('private/port.json')
    port=portJson['port']

    utilities.send_email([email], 'Hydra Event Server Verification', 'Your Verification Code Is:\n\n  ' + code + '\n\nFollow the link to http://' + url + ":" + str(port) + '/verify and enter the information to verify your account.\n\nThank you,\n\nThe Hydra Event Manager Team', constants.MAIL)

if __name__ == '__main__':
    load_private_key()
    portJson = utilities.load_json_file('private/port.json')
    hostJson = utilities.load_json_file('private/url.json')

    if utilities.file_exists('private/mail.json'):
        mailInfo = utilities.load_json_file('private/mail.json')
        app.config['MAIL_SERVER']=mailInfo['server']
        app.config['MAIL_PORT'] = mailInfo['port']
        app.config['MAIL_USERNAME'] = mailInfo['uname']
        app.config['MAIL_PASSWORD'] = mailInfo['password']
        app.config['MAIL_USE_TLS'] = True
        constants.MAIL = Mail(app)

    app.run(debug=True, port=portJson['port'], host=hostJson['url'])