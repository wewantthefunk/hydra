from hydra import app
import constants, utilities, sys
from flask_mail import Mail

if __name__ == '__main__':

    if len(sys.argv) < 2:
        constants.DB_LOCATION = "data/user_db.db"
    else:
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

    app.run(debug=False, port=portJson['port'], host=hostJson['url'])