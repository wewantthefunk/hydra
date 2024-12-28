import dataaccess, constants, crypto_asymmetric, crypto_symmetric, utilities
import base64
from datetime import datetime

def login(username: str, password: str, temp_password: str):
    tempPassword = decrypt_string(temp_password)
    uname = decrypt_string(username)

    rows = dataaccess.get_user(uname)

    if len(rows) != 1:
        return {'result': constants.RESULT_FORBIDDEN, "message": 'Invalid Username and Password'}

    password = decrypt_string(password)

    passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0].passphrase) , password.encode('utf-8'))

    level = str(rows[0].user_type)

    if rows[0].is_verified == constants.UNVERIFIED_ACCOUNT:
        return {'message': 'Your Account is Not Verified', 'result': constants.RESULT_UNVERIFIED_ACCOUNT}
    elif passphrase == 'valid password: ' + uname:
        token = utilities.generate_random_string(15)
        jdate = utilities.date_to_julian(datetime.now())
        result = dataaccess.create_user_session(jdate, uname, token)
        if (result):
            #tp = base64.b64encode(crypto_symmetric.encrypt(token, tempPassword.encode('utf-8'))).decode('ascii')
            tp = tempPassword
            return {'result': constants.RESULT_OK, 'tmp_password': tp, 'level': level}
        else:
            return {"message": "Server Error", 'result': constants.RESULT_UNVERIFIED_ACCOUNT }
    else:
        return {'message': 'Invalid Username and Password', 'result': constants.RESULT_FORBIDDEN }
    
def create_account(email: str, password: str, username: str):
    email = decrypt_string(email)
    password = decrypt_string(password)
    username = decrypt_string(username)

    rows = dataaccess.get_user_by_email_or_username(email = email, username=username)

    if len(rows) > 0:
        return {'message': 'Username and/or Email already registered', 'result': constants.RESULT_INVALID_REQUEST}
    
    passphrase = 'valid password: ' + username

    p = crypto_symmetric.encrypt(passphrase, password.encode('utf-8'))

    vcode = utilities.generate_random_string(6)

    result = dataaccess.create_account(username, base64.b64encode(p).decode('ascii'), email, vcode)

    if result:
        return {'message': 'Account Created', 'result': constants.RESULT_OK, 'email': email, 'vcode': vcode} 
    
    return {'message': 'Server Error', 'result': constants.RESULT_SERVER_ERROR}

def check_admin(username: str):
    username = decrypt_string(username)

    rows = dataaccess.check_admin(username)

    if len(rows) > 0:
        r = constants.RESULT_OK
        m = 'User Is Admin'
        if rows[0].is_verified == constants.UNVERIFIED_ACCOUNT:
            r = constants.RESULT_UNVERIFIED_ACCOUNT
            m = "Unverified Account"
        return {'message': m, 'result': r, 'email': rows[0].email, 'vcode': rows[0].verification_code, 'is_verified': rows[0].is_verified}
    
    return {'message': "User Is NOT Admin", 'result': constants.RESULT_FORBIDDEN}

def generate_verify(email: str):
    e = decrypt_string(e)

    rows = dataaccess.get_user_by_email(e)

    if len(rows) < 1:
        return {'message': 'Email Does Not Exist', 'result': constants.RESULT_INVALID_REQUEST}
    
    if rows[0].is_verified == constants.VERIFIED_ACCOUNT:
        return {'message': 'Account Already Verified', 'result': constants.RESULT_ALREADY_VERIFIED}
    
    vcode = utilities.generate_random_string(6)

    result = dataaccess.update_user_verification_code(email=e, vcode=vcode)

    if result:
        return {'message': 'Verification Code Generated', 'result': constants.RESULT_OK, 'email': e, 'vcode': vcode}

def verify_account(email: str, password: str, code: str):
    e = decrypt_string(email)
    p = decrypt_string(password)
    c = decrypt_string(code)

    rows = dataaccess.get_user_by_email_and_verification_code(email=e, code=c)

    if len(rows) < 1:
        return {'message': 'Invalid Verification Information', 'result': constants.RESULT_FORBIDDEN}
    
    passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0].passphrase) , p.encode('utf-8'))

    if passphrase != 'valid password: ' + rows[0].username:
        return {'message': 'Invalid Verification Information', 'result': constants.RESULT_FORBIDDEN}

    result = dataaccess.verify_account(rows[0].id, passphrase=passphrase)

    return result

def check_token(token: str, username: str):
    t = decrypt_string(token)
    u = decrypt_string(username)

    jdate = utilities.date_to_julian(datetime.now())   

    rows = dataaccess.get_session_by_username_token_and_issued(jdate=jdate, uname=u, token=t) 

    if len(rows) < 1:
        return {'message': 'Invalid Token', 'result': constants.RESULT_FORBIDDEN}
    
    return {'message': 'success', 'result': constants.RESULT_OK}

def decrypt_string(s: str):
    return s
    #byte_array = base64.b64decode(s)
    #u = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

    #return u
