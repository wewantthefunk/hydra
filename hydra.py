from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
import utilities, constants, businesslogic
import sys

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
            
        return jsonify({'message': 'Successful Login', 'token': result['token'], 'level': result['level']}), constants.RESULT_OK
    
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

        result = businesslogic.check_token(processed_data['token'], processed_data['username'])
        
        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'error': "Invalid Request"}), constants.RESULT_INVALID_REQUEST
    
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

        result = businesslogic.verify_account(processed_data['email'], processed_data['password'], processed_data['code'])        

        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'error': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route('/generateverify', methods=['POST'])
def generateverify():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1')
        }

        result = businesslogic.generate_verify(processed_data['email'])
        
        if result['result'] == constants.RESULT_OK:
            send_verification_email(result['email'], result['vcode'])

            return jsonify({'message': 'Verification Email Sent'}), constants.RESULT_OK

    return jsonify({'error': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route("/checkadmin", methods=['POST'])
def checkAdminVerification():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'username': data.get('field3')
        }

        result = businesslogic.check_admin(processed_data['username'])

        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'error': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

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

        result = businesslogic.create_account(processed_data['email'], processed_data['password'], processed_data['username'])

        if result['result'] == constants.RESULT_OK:
            send_verification_email(result['email'], result['vcode'])

            return jsonify({'message': 'Account Creation Successful! You must verify your account before you can login!'}), constants.RESULT_OK
        
        return jsonify({"error": result['message']}), result['result']
    
    return jsonify({'error': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

def send_verification_email(email: str, code: str):
    hostJson = utilities.load_json_file('private/url.json')
    url = hostJson['url']

    portJson = utilities.load_json_file('private/port.json')
    port=portJson['port']

    utilities.send_email([email], 'Hydra Event Server Verification', 'Your Verification Code Is:\n\n  ' + code + '\n\nFollow the link to http://' + url + ":" + str(port) + '/verify and enter the information to verify your account.\n\nThank you,\n\nThe Hydra Event Manager Team', constants.MAIL)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Path to SQLite database file required!")
        exit(1000)

    constants.DB_LOCATION = sys.argv[1]
    
    utilities.load_private_key()
    mailInfo = utilities.load_mail_server_info()

    app.config['MAIL_SERVER']=mailInfo['server']
    app.config['MAIL_PORT'] = mailInfo['port']
    app.config['MAIL_USERNAME'] = mailInfo['uname']
    app.config['MAIL_PASSWORD'] = mailInfo['password']
    app.config['MAIL_USE_TLS'] = True
    constants.MAIL = Mail(app)

    portJson = utilities.load_json_file('private/port.json')
    hostJson = utilities.load_json_file('private/url.json')

    app.run(debug=True, port=portJson['port'], host=hostJson['url'])