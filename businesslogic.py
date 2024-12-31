import dataaccess, constants, crypto_asymmetric, crypto_symmetric, utilities
import base64
from datetime import datetime

def login(username: str, password: str, temp_password: str, encrypt: bool):
    tempPassword = decrypt_string(temp_password, encrypt)
    uname = decrypt_string(username, encrypt)

    rows = dataaccess.get_user_by_email_or_username(uname, uname)

    if len(rows) != 1:
        return {'result': constants.RESULT_FORBIDDEN, "message": 'Invalid Username and Password'}

    password = decrypt_string(password, encrypt)

    passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0].passphrase) , password.encode('utf-8'))

    level = str(rows[0].user_type)

    if rows[0].is_verified == constants.UNVERIFIED_ACCOUNT:
        return {'message': 'Your Account is Not Verified', 'result': constants.RESULT_UNVERIFIED_ACCOUNT}
    elif passphrase == 'valid password: ' + rows[0].username:
        token = utilities.generate_random_string(15)
        jdate = utilities.date_to_julian(datetime.now())
        result = dataaccess.create_user_session(jdate, uname, token)
        if (result):
            tp = decrypt_symmetric_string(token, tempPassword, encrypt)
            return {'result': constants.RESULT_OK, 'token': tp, 'level': level, 'uname': rows[0].username}
        else:
            return {"message": "Server Error", 'result': constants.RESULT_UNVERIFIED_ACCOUNT }
    else:
        return {'message': 'Invalid Username and Password', 'result': constants.RESULT_FORBIDDEN }
    
def create_account(email: str, password: str, username: str, encrypt: bool):
    email = decrypt_string(email, encrypt=encrypt)
    password = decrypt_string(password, encrypt)
    username = decrypt_string(username, encrypt)

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

def check_admin(username: str, encrypt: bool):
    username = decrypt_string(username, encrypt)

    rows = dataaccess.check_admin(username)

    if len(rows) > 0:
        r = constants.RESULT_OK
        m = 'User Is Admin'
        if rows[0].is_verified == constants.UNVERIFIED_ACCOUNT:
            r = constants.RESULT_UNVERIFIED_ACCOUNT
            m = "Unverified Account"
        return {'message': m, 'result': r, 'email': rows[0].email, 'vcode': rows[0].verification_code, 'is_verified': rows[0].is_verified}
    
    return {'message': "User Is NOT Admin", 'result': constants.RESULT_FORBIDDEN}

def check_organizer(username: str, encrypt: bool):
    username = decrypt_string(username, encrypt)

    rows = dataaccess.check_organizer(username)

    if len(rows) > 0:
        r = constants.RESULT_OK
        m = 'User Is Admin'
        if rows[0].is_verified == constants.UNVERIFIED_ACCOUNT:
            r = constants.RESULT_UNVERIFIED_ACCOUNT
            m = "Unverified Account"
        return {'message': m, 'result': r, 'email': rows[0].email, 'vcode': rows[0].verification_code, 'is_verified': rows[0].is_verified}
    
    return {'message': "User Is NOT Admin", 'result': constants.RESULT_FORBIDDEN}

def generate_verify(email: str, encrypt: bool):
    e = decrypt_string(email, encrypt)

    rows = dataaccess.get_user_by_email(e)

    if len(rows) < 1:
        return {'message': 'Email Does Not Exist', 'result': constants.RESULT_INVALID_REQUEST}
    
    if rows[0].is_verified == constants.VERIFIED_ACCOUNT:
        return {'message': 'Account Already Verified', 'result': constants.RESULT_ALREADY_VERIFIED}
    
    vcode = utilities.generate_random_string(6)

    result = dataaccess.update_user_verification_code(email=e, vcode=vcode)

    if result:
        return {'message': 'Verification Code Generated', 'result': constants.RESULT_OK, 'email': e, 'vcode': vcode}

def verify_account(email: str, password: str, code: str, encrypt: bool):
    e = decrypt_string(email, encrypt)
    p = decrypt_string(password, encrypt)
    c = decrypt_string(code, encrypt)

    rows = dataaccess.get_user_by_email_and_verification_code(email=e, code=c)

    if len(rows) < 1:
        return {'message': 'Invalid Verification Information', 'result': constants.RESULT_FORBIDDEN}
    
    passphrase = crypto_symmetric.decrypt(base64.b64decode(rows[0].passphrase) , p.encode('utf-8'))

    if passphrase != 'valid password: ' + rows[0].username:
        return {'message': 'Invalid Verification Information', 'result': constants.RESULT_FORBIDDEN}

    result = dataaccess.verify_account(rows[0].id, passphrase=passphrase)

    return result

def check_token(token: str, username: str, encrypt: bool):
    t = decrypt_string(token, encrypt)
    u = decrypt_string(username, encrypt)

    jdate = utilities.date_to_julian(datetime.now())   

    rows = dataaccess.get_session_by_username_token_and_issued(jdate=jdate, uname=u, token=t) 

    if len(rows) < 1:
        return {'message': 'Invalid Token', 'result': constants.RESULT_FORBIDDEN}
    
    rows = dataaccess.get_user(rows[0].username)

    return {'message': 'success', 'userId': rows[0].id, 'result': constants.RESULT_OK}

def check_token_post(token: str, username: str, encrypt: bool):
    token_r = check_token(token, username, encrypt)

    if (token_r['result'] != constants.RESULT_OK):
        return [False, token_r]

    return [True, token_r]

def check_admin_post(username: str, encrypt: bool) -> bool:
    admin_r = check_admin(username, encrypt)

    if (admin_r['result'] != constants.RESULT_OK):
        return False
    
    return True

def check_organizer_post(username: str, encrypt: bool) -> bool:
    organizer_r = check_organizer(username, encrypt)

    if (organizer_r['result'] != constants.RESULT_OK):
        return False
    
    return True

def decrypt_string(s: str, encrypt: bool = False) -> str:
    if encrypt:
        if constants.PRIVATE_KEY is None:
            utilities.load_private_key()

        byte_array = base64.b64decode(s)
        u = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        return u
    
    return s

def decrypt_symmetric_string(s: str, p: str, encrypt: bool = False) -> str:
    if encrypt:
        return base64.b64encode(crypto_symmetric.encrypt(s, p.encode('utf-8'))).decode('ascii')
    
    return s

def unverify_user(name: str) -> bool:
    rows = dataaccess.get_user_by_email_or_username(name, name)

    if len(rows) < 1:
        print("User Not Found")
        return False
    
    return dataaccess.unverify_user(rows[0].id)

def create_new_event(userId: int, name: str, startdate: str, enddate: str, starttime: str, endtime: str, location: str, invite_only: str, max: str, code: str, encrypt: bool = False) -> str:
    n = decrypt_string(name, encrypt)
    sd = decrypt_string(startdate, encrypt)
    ed = decrypt_string(enddate, encrypt)
    st = decrypt_string(starttime, encrypt)
    et = decrypt_string(endtime, encrypt)
    l = decrypt_string(location, encrypt)
    io = decrypt_string(invite_only, encrypt)
    if io == 'true':
        io = '1'
    else:
        io = '0'
    m = decrypt_string(max, encrypt)
    c = decrypt_string(code, encrypt)

    ev = dataaccess.get_event_by_userid_and_name_or_invite_code(userId, n, c)

    if ev.id > 0:
        return {'message': 'Event Already Exists', 'id': ev.id, 'result': constants.RESULT_CONFLICT}

    id = dataaccess.create_event(userId, n, sd, ed, st, et, l, io, m, c)

    return {'message': 'Event Created', 'id': str(id), 'result': constants.RESULT_OK}
