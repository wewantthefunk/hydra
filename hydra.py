from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
import utilities, constants, businesslogic

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

@app.route('/outpublicevents')
def outpublicevents():
    return render_template('out-public-events.html', app_name=constants.APP_NAME)

@app.route("/verify")
def verify():
    return render_template("out-verify.html", app_name=constants.APP_NAME)

@app.route("/account")
def account():
    return render_template("in-account.html", app_name=constants.APP_NAME)

@app.route("/admin")
def admin():
    return render_template("in-admin.html", app_name=constants.APP_NAME)

@app.route("/publicevents")
def publicevents():
    return render_template('in-public-events.html', app_name=constants.APP_NAME)

@app.route('/getusers', methods=['POST'])
def getusers():
    pass

@app.route('/getpublicevents')
def getpublicevents():
    result = businesslogic.get_public_events()

    return jsonify({'message': result['message']}), constants.RESULT_OK

@app.route('/attend/<invite>')
def attend(inviteCode):
    pass

@app.route('/myevents', methods=['POST'])
def my_events():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'token': data.get('field1'),
            'username': data.get('field2'),
            'e': data.get('e')
        }

        rt = businesslogic.check_token_post(processed_data['token'], processed_data['username'], processed_data['e'])

        if not rt[0]:
            return jsonify({'message': rt[1]['message']}), rt[1]['result']
        
        result = businesslogic.get_my_events(rt[1]['userId'])

        return jsonify({'message': result['message']}), constants.RESULT_OK
    
    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'username': data.get('field1'),
            'password': data.get('field2'),
            'tempPassword': data.get('field3'),
            'e': data.get('e')
        }

        result = businesslogic.login(processed_data['username'], processed_data['password'], processed_data['tempPassword'], utilities.use_encrypt(processed_data['e']))

        if result['result'] != constants.RESULT_OK:
            return jsonify({'error': result['message']}), result['result']
            
        return jsonify({'message': 'Successful Login', 'token': result['token'], 'level': result['level'], 'uname': result['uname']}), constants.RESULT_OK
    
    return jsonify({'message': 'Invalid Request'}), constants.RESULT_INVALID_REQUEST

@app.route("/check", methods=['POST'])
def checkToken():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'token': data.get('field1'),
            'username': data.get('field2'),
            'e': data.get('e')
        }

        result = businesslogic.check_token(processed_data['token'], processed_data['username'], utilities.use_encrypt(processed_data['e']))
        
        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST
    
@app.route('/verifyaccount', methods=['POST'])
def verifyaccount():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'code': data.get('field3'),
            'e': data.get('e')
        }

        result = businesslogic.verify_account(processed_data['email'], processed_data['password'], processed_data['code'], utilities.use_encrypt(processed_data['e']))        

        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route('/generateverify', methods=['POST'])
def generateverify():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'e': data.get('e')
        }

        result = businesslogic.generate_verify(processed_data['email'], utilities.use_encrypt(processed_data['e']))
        
        if result['result'] == constants.RESULT_OK:
            send_verification_email(result['email'], result['vcode'])

            return jsonify({'message': 'Verification Email Sent', 'status': result['result'], 'result': result['message']}), result['result']

    return jsonify({'message': "Invalid Request", 'message': result['message'], 'status': str(result['result'])}), result['result']

@app.route("/checkadmin", methods=['POST'])
def checkAdminVerification():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'username': data.get('field3'),
            'e': data.get('e')
        }

        result = businesslogic.check_admin(processed_data['username'], utilities.use_encrypt(processed_data['e']))

        return jsonify({'message': result['message']}), result['result']
    
    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route("/createaccount", methods=['POST'])
def createaccount():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'email': data.get('field1'),
            'password': data.get('field2'),
            'username': data.get('field3'),
            'e': data.get('e')
        }

        result = businesslogic.create_account(processed_data['email'], processed_data['password'], processed_data['username'], utilities.use_encrypt(processed_data['e']))

        if result['result'] == constants.RESULT_OK:
            send_verification_email(result['email'], result['vcode'])

            return jsonify({'message': 'Account Creation Successful! You must verify your account before you can login!'}), constants.RESULT_OK
        
        return jsonify({"message": result['message']}), result['result']
    
    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

@app.route('/createevent', methods=['POST'])
def create_event():
    if request.is_json:
        data = request.get_json()

        # Process the JSON data here as needed
        processed_data = {
            'token': data.get('field1'),
            'eventname': data.get('field2'),
            'startdate': data.get('field3'),
            'enddate': data.get('field4'),
            'location': data.get('field5'),
            'max': data.get('field6'),
            'isinvite': data.get('field7'),
            'code': data.get('field8'),
            'e': data.get('e'),
            'uname': data.get('field9'),
            'starttime': data.get('field10'),
            'endtime': data.get('field11')
        }

        session = businesslogic.check_token_post(processed_data['token'], processed_data['uname'], processed_data['e'])

        if not session[0]:
            return jsonify({'message': "User Not Authorized to Create Events"}), constants.RESULT_FORBIDDEN
        
        r = businesslogic.check_organizer_post(processed_data['uname'], processed_data['e'])

        if not r:
            return jsonify({'message': "User Not Authorized to Create Events"}), constants.RESULT_FORBIDDEN
        

        r = businesslogic.create_new_event(session[1]['userId'],
                                           processed_data['eventname'],
                                           processed_data['startdate'],
                                           processed_data['enddate'],
                                           processed_data['starttime'],
                                           processed_data['endtime'],
                                           processed_data['location'],
                                           processed_data['isinvite'],
                                           processed_data['max'],
                                           processed_data['code'],
                                           processed_data['e'])

        return jsonify({'message': r['message']}), r['result']

    return jsonify({'message': "Invalid Request"}), constants.RESULT_INVALID_REQUEST

def send_verification_email(email: str, code: str):
    hostJson = utilities.load_json_file('private/url.json')
    url = hostJson['url']

    portJson = utilities.load_json_file('private/port.json')
    port=portJson['port']

    if constants.MAIL == None:
        mailInfo = utilities.load_mail_server_info()

        app.config['MAIL_SERVER']=mailInfo['server']
        app.config['MAIL_PORT'] = mailInfo['port']
        app.config['MAIL_USERNAME'] = mailInfo['uname']
        app.config['MAIL_PASSWORD'] = mailInfo['password']
        app.config['MAIL_USE_TLS'] = True
        constants.MAIL = Mail(app)

    utilities.send_email([email], 'Hydra Event Server Verification', 'Your Verification Code Is:\n\n  ' + code + '\n\nFollow the link to http://' + url + ":" + str(port) + '/verify and enter the information to verify your account.\n\nThank you,\n\nThe Hydra Event Manager Team', constants.MAIL)

if __name__ == '__main__':  
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