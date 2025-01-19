import dataaccess, constants, crypto_asymmetric, crypto_symmetric, utilities
import base64, sys
from datetime import datetime
import stripe

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
        return {'message': 'Invalid Token', 'userId': -1, 'result': constants.RESULT_FORBIDDEN}

    return {'message': 'success', 'userId': rows[0].id, 'result': constants.RESULT_OK}

def check_token_post(token: str, username: str, encrypt: bool):
    token_r = check_token(token, username, encrypt)

    if (token_r['result'] != constants.RESULT_OK):
        return [False, token_r]

    return [True, token_r]

def get_user_by_name(username: str, encrypt: bool):
    u = decrypt_string(username, encrypt)

    result = dataaccess.get_user_by_email_or_username(u, u)

    if len(result) < 1:
        return dataaccess.User('', '', -1, '', '', False, '00000', False)
    
    return {
        "email": result[0].email,
        "username": result[0].username,
        "id": result[0].id,
        "type": result[0].user_type
    }

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
    e = utilities.str_to_bool(str(encrypt))

    if e:
        if constants.PRIVATE_KEY is None:
            utilities.load_private_key()

        byte_array = base64.b64decode(s)
        u = crypto_asymmetric.rsa_decrypt(private_key=constants.PRIVATE_KEY, encrypted_message=byte_array)

        return u
    
    return s

def decrypt_symmetric_string(s: str, p: str, encrypt: bool = False) -> str:
    e = utilities.str_to_bool(str(encrypt))

    if e:
        return base64.b64encode(crypto_symmetric.encrypt(s, p.encode('utf-8'))).decode('ascii')
    
    return s

def unverify_user(name: str) -> bool:
    rows = dataaccess.get_user_by_email_or_username(name, name)

    if len(rows) < 1:
        print("User Not Found")
        return False
    
    return dataaccess.unverify_user(rows[0].id)

def create_new_event(userId: int, name: str, startdate: str, enddate: str, starttime: str, endtime: str, location: str, invite_only: str, max: str, code: str, allow_anonymous_signups: str, require_signin: str, payment_type: str, cost: str, sku: str, update_or_create: str, id: str, last_cancel: str, organizerAsAttendee: str, encrypt: bool = False) -> str:
    n = decrypt_string(name, encrypt)
    sd = decrypt_string(startdate, encrypt)
    ed = decrypt_string(enddate, encrypt)
    st = decrypt_string(starttime, encrypt)
    et = decrypt_string(endtime, encrypt)
    l = decrypt_string(location, encrypt)
    io = decrypt_string(invite_only, encrypt)
    m = decrypt_string(max, encrypt)
    c = decrypt_string(code, encrypt)
    aas = decrypt_string(allow_anonymous_signups, encrypt)
    rsi = decrypt_string(require_signin, encrypt)
    uorc = decrypt_string(update_or_create, encrypt)
    eid = decrypt_string(id, encrypt)
    pt = decrypt_string(payment_type, encrypt)
    co = decrypt_string(cost, encrypt)
    s = decrypt_string(sku, encrypt)
    lc = decrypt_string(last_cancel, encrypt)
    oaa = decrypt_string(organizerAsAttendee, encrypt)

    ev = dataaccess.get_event_by_userid_and_name_or_invite_code(userId, n, c)

    if uorc == 'new':
        if ev.id > 0:
            return {'message': 'Event Already Exists', 'id': ev.id, 'result': constants.RESULT_CONFLICT}

        id = dataaccess.create_event(userId, n, sd, ed, st, et, l, io, m, c, aas, rsi, pt, co, s, lc, oaa)

        return {'message': 'Event Created', 'id': str(id), 'result': constants.RESULT_OK}
    else:
        if ev.id <= 0:
            return {'message': 'Event Does Not Exist, Unable to Update', 'id': eid, 'result': constants.RESULT_NOT_FOUND}
        
        eid = dataaccess.update_event(userId, n, sd, ed, st, et, l, io, m, c, aas, eid, rsi, pt, co, s, lc, oaa)

        return {'message': 'Event Updated', 'id': str(eid), 'result': constants.RESULT_OK}

def get_public_events():
    events = dataaccess.get_public_events()

    events_out = ''

    first = True
    for event in events:
        e = ''

        if not first:
            e = e + ','

        e = e + '{'
        e = e + '"id":' + str(event.id) + ","
        e = e + '"name":"' + event.name + '",'
        e = e + '"startDate":"' + event.start_date + '",'
        e = e + '"endDate":"' + event.end_date + '",'
        e = e + '"startTime":"' + event.start_time + '",'
        e = e + '"endTime":"' + event.end_time + '",'
        e = e + '"maxAttendees":' + str(event.max_attendees) + ','
        e = e + '"currentAttendees":' + str(event.current_attendees) + ','
        e = e + '"location":"' + event.location + '",'
        e = e + '"inviteType":' + str(event.invite_only) + ','
        e = e + '"inviteCode":"' + event.invite_code + '",'
        e = e + '"allowAnonymousAttendees":' + str(event.allow_anonymous_signups) + ","
        e = e + '"requireSignIn":' + str(event.require_signin) + ","
        e = e + '"cost":' + str(event.cost) + ","
        e = e + '"paymentType":' + str(event.payment_required) + ","
        e = e + '"sku":"' + event.sku + '",'
        e = e + '"relationship":' + str(event.relationship)
        e = e + '}'


        first = False
        events_out = events_out + e
    
    return {'message': '{"events":[' + events_out + ']}', 'id': '-1', 'result': constants.RESULT_OK}

def get_my_events(user_id: int):
    events = dataaccess.get_my_events(user_id)

    events_out = ''

    first = True
    for event in events:
        e = ''

        if not first:
            e = e + ','

        e = e + '{'
        e = e + '"id":' + str(event.id) + ","
        e = e + '"name":"' + event.name + '",'
        e = e + '"startDate":"' + event.start_date + '",'
        e = e + '"endDate":"' + event.end_date + '",'
        e = e + '"startTime":"' + event.start_time + '",'
        e = e + '"endTime":"' + event.end_time + '",'
        e = e + '"maxAttendees":' + str(event.max_attendees) + ','
        e = e + '"currentAttendees":' + str(event.current_attendees) + ','
        e = e + '"location":"' + event.location + '",'
        e = e + '"inviteType":' + str(event.invite_only) + ','
        e = e + '"inviteCode":"' + event.invite_code + '",'
        e = e + '"allowAnonymousAttendees":' + str(event.allow_anonymous_signups) + ","
        e = e + '"requireSignIn":' + str(event.require_signin) + ","
        e = e + '"cost":' + str(event.cost) + ","
        e = e + '"paymentType":' + str(event.payment_required) + ","
        e = e + '"sku":"' + event.sku + '",'
        e = e + '"relationship":' + str(event.relationship) + ','
        e = e + '"lastCancel":"' + event.last_cancel + '",'
        e = e + '"organizerAsAttendee":' + str(event.organizer_as_attendee)
        e = e + '}'


        first = False
        events_out = events_out + e
    
    return {'message': '{"events":[' + events_out + ']}', 'id': '-1', 'result': constants.RESULT_OK}

def delete_event(user_id: int, event_id: int, encrypt: bool = False):
    eid = decrypt_string(event_id, encrypt)

    result = dataaccess.delete_event(user_id, eid)

    if result:
        return {'message': 'Event Deleted', 'result': constants.RESULT_OK}
    
    return {'message': 'Event Not Deleted', 'result': constants.RESULT_INVALID_REQUEST}

def check_attendance(user_id: str, invite: str, encrypt: str):
    i = decrypt_string(invite, encrypt)

    result = dataaccess.check_attendance(user_id, i)

    if not result[0]:
        return {'message': 'Already Attending', 'reason': result[1], 'result': constants.RESULT_ALREADY_ATTENDING}
    
    return {'message': 'Not Attending', 'reason': result[1], 'result': constants.RESULT_OK}

def get_event(invite: str, encrypt: str):
    i = decrypt_string(invite, encrypt)

    event = dataaccess.get_event(i)

    e = '{'
    e = e + '"id":' + str(event.id) + ","
    e = e + '"name":"' + event.name + '",'
    e = e + '"startDate":"' + event.start_date + '",'
    e = e + '"endDate":"' + event.end_date + '",'
    e = e + '"startTime":"' + event.start_time + '",'
    e = e + '"endTime":"' + event.end_time + '",'
    e = e + '"maxAttendees":' + str(event.max_attendees) + ','
    e = e + '"currentAttendees":' + str(event.current_attendees) + ','
    e = e + '"location":"' + event.location + '",'
    e = e + '"inviteType":' + str(event.invite_only) + ','
    e = e + '"inviteCode":"' + event.invite_code + '",'
    e = e + '"allowAnonymousAttendees":' + str(event.allow_anonymous_signups) + ","
    e = e + '"requireSignIn":' + str(event.require_signin) + ","
    e = e + '"cost":' + str(event.cost) + ","
    e = e + '"paymentType":' + str(event.payment_required) + ","
    e = e + '"sku":"' + event.sku + '",'
    e = e + '"relationship":' + str(event.relationship) + ","
    e = e + '"organizerAsAttendee":' + str(event.organizer_as_attendee) + ","
    e = e + '"lastCancel":"' + event.last_cancel + '"'
    e = e + '}'
    
    return {'message': e, 'result': constants.RESULT_OK}

def checkout(full_url: str, sku: str, quantity: str, encrypt: str) -> str:
    s = decrypt_string(sku, encrypt)
    q = decrypt_string(quantity, encrypt)

    try: 
        price_id = 'ID'
        cost = 1.0

        stripe_api_key = utilities.load_json_file("private/stripe-api-key.json")

        for price in stripe_api_key['prices']:
            if price['sku'] == s:
                price_id = price['price_id']
                cost = price['price']
                break

        if cost == 0.0:
            return {"url":'success.html','sessionId':constants.FREE_EVENT_RECEIPT,'message':'checkout complete','result': constants.RESULT_OK}

        stripe.api_key = stripe_api_key['stripe-test']

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price_id,
                    'quantity': int(q)
                },
            ],
            mode='payment',
            success_url=full_url + '/success.html',
            cancel_url=full_url + '/cancel.html',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return {'message':str(e), 'url': 'none.html', 'sessionId': 'none', 'result': constants.RESULT_INVALID_REQUEST}
    
    return {"url":checkout_session.url, "sessionId": checkout_session.id, "message": 'checkout session started', 'result': constants.RESULT_OK}

def get_payment_info(sesssion_id: str, encrypt: str):
    sid = decrypt_string(sesssion_id, encrypt)

    if sid == constants.FREE_EVENT_RECEIPT:
        return {'receipt': constants.FREE_EVENT_RECEIPT, 'receipt_url':constants.FREE_RECEIPT_URL, 'receipt_id': constants.FREE_RECEIPT_ID, 'result': constants.RESULT_OK}

    stripe_api_key = utilities.load_json_file("private/stripe-api-key.json")

    stripe.api_key = stripe_api_key['stripe-test']

    session = stripe.checkout.Session.retrieve(
            sid,
            expand=[],
        )

    charge = stripe.Charge.retrieve(stripe.PaymentIntent.retrieve(session['payment_intent'])['latest_charge'])

    return {"receipt": charge['receipt_number'], "receipt_url": charge['receipt_url'], 'receipt_id': charge['id'], "result": constants.RESULT_OK}

def issue_refund(charge_id: str, encrypt: str):
    cid = decrypt_string(charge_id, encrypt)

    stripe_api_key = utilities.load_json_file("private/stripe-api-key.json")

    stripe.api_key = stripe_api_key['stripe-test']

    charge = stripe.Charge.retrieve(cid)

    refund = stripe.Refund.create(payment_intent=charge['payment_intent'])

    return refund

def mark_attended(invite: str, userid: str, receipt_id: str, receipt_num: str, receipt_url: str, encrypt: str):
    i = decrypt_string(invite, encrypt)
    rid = decrypt_string(receipt_id, encrypt)
    rn = decrypt_string(receipt_num, encrypt)
    rurl = decrypt_string(receipt_url, encrypt)

    result = dataaccess.mark_attended(userid, i, rid, rn, rurl)

    if not result[0]:
        return {'message': 'Unable to Attend', 'result': constants.RESULT_INVALID_REQUEST}
    
    return {'message': 'Attending', 'badge_number': result[1], 'result': constants.RESULT_OK}

def mark_skipped(invite: str, userid: str, encrypt: str):
    i = decrypt_string(invite, encrypt)

    result = dataaccess.mark_skipped(userid, i)

    if not result[0]:
        return {'message': 'Unable to Skip', 'result': constants.RESULT_INVALID_REQUEST}
    
    id = 'free'

    if result[1] != '':
        stripe_api_key = utilities.load_json_file("private/stripe-api-key.json")
        stripe.api_key = stripe_api_key['stripe-test']

        charge = stripe.Charge.retrieve(id=result[1])

        refund = stripe.Refund.create(payment_intent=charge.payment_intent)

        id = refund.id

        if (refund.status != 'succeeded'):
            return {'message': "Error Issuing Refund", 'refund': 'error', result: constants.RESULT_SERVER_ERROR}
    
    return {'message': 'Skipped', 'refund': id, 'result': constants.RESULT_OK}

def get_attendance_info(invite: str, userid: str, encrypt: str):
    i = decrypt_string(invite, encrypt)

    result = dataaccess.get_attendance_info(userid, i)

    if not result[0]:
        return {'message': 'Not Attending', 'badge_number': '', 'receipt_id': '', 'receipt_num': '', 'receipt_url': '', 'result': constants.RESULT_NOT_FOUND}
    
    return {'message': 'Attending', 
            'badge_number': result[1], 
            'receipt_id': result[2],
            'receipt_num': result[3],
            'receipt_url': result[4],
            'result': constants.RESULT_OK}

def update_username(current_username: str, new_username: str, pw: str, token: str, encrypt: str):
    cu = decrypt_string(current_username, encrypt)
    nu = decrypt_string(new_username, encrypt)
    pwd = decrypt_string(pw, encrypt)

    exists = dataaccess.get_user(nu)

    if len(exists) > 0:
        return {'message': 'Username already exists', 'result': constants.RESULT_CONFLICT}
    
    exists = dataaccess.get_user(cu)

    if len(exists) < 1:
        return {'message': 'Current username not found', 'result': constants.RESULT_NOT_FOUND}
    
    passphrase = crypto_symmetric.decrypt(base64.b64decode(exists[0].passphrase) , pwd.encode('utf-8'))

    if passphrase != 'valid password: ' + exists[0].username:
        return {'message': 'Invalid Password', 'result': constants.RESULT_FORBIDDEN}
    
    passphrase = 'valid password: ' + nu

    p = crypto_symmetric.encrypt(passphrase, pwd.encode('utf-8'))

    u = dataaccess.update_username(str(exists[0].id), nu, base64.b64encode(p).decode('ascii'), token)

    if u.id > 0:
        return {'message': 'Username Updated', 'result': constants.RESULT_OK}
    
    return {'message': 'Invalid', 'result': constants.RESULT_SERVER_ERROR}

def update_email(current_email: str, new_email: str, pw: str, token: str, encrypt: str):
    ce = decrypt_string(current_email, encrypt)
    ne = decrypt_string(new_email, encrypt)
    pwd = decrypt_string(pw, encrypt)

    exists = dataaccess.get_user_by_email(ne)

    if len(exists) > 0:
        return {'message': 'Email already exists', 'result': constants.RESULT_CONFLICT}
    
    exists = dataaccess.get_user_by_email(ce)

    if len(exists) < 1:
        return {'message': 'Current email not found', 'result': constants.RESULT_NOT_FOUND}
    
    passphrase = crypto_symmetric.decrypt(base64.b64decode(exists[0].passphrase) , pwd.encode('utf-8'))

    if passphrase != 'valid password: ' + exists[0].username:
        return {'message': 'Invalid Password', 'result': constants.RESULT_FORBIDDEN}

    u = dataaccess.update_email(str(exists[0].id), ne, token)

    if u.id > 0:
        return {'message': 'Email Updated', 'result': constants.RESULT_OK}
    
    return {'message': 'Invalid', 'result': constants.RESULT_SERVER_ERROR}

def update_password(new_password: str, password: str, user_id: int, encrypt: str):
    npwd = decrypt_string(new_password, encrypt)
    pwd = decrypt_string(password, encrypt)

    exists = dataaccess.get_user_by_userid(user_id)

    if len(exists) < 1:
        return {'message': 'User Not Found', 'result': constants.RESULT_NOT_FOUND}
    
    passphrase = crypto_symmetric.decrypt(base64.b64decode(exists[0].passphrase) , pwd.encode('utf-8'))

    if passphrase != 'valid password: ' + exists[0].username:
        return {'message': 'Invalid Password', 'result': constants.RESULT_FORBIDDEN}
    
    new_passphrase =  crypto_symmetric.encrypt(passphrase, npwd.encode('utf-8'))

    u = dataaccess.update_password(str(exists[0].id), base64.b64encode(new_passphrase).decode('ascii'))

    if u.id > 0:
        return {'message': 'Password Updated', 'result': constants.RESULT_OK}
    
    return {'message': 'Invalid', 'result': constants.RESULT_SERVER_ERROR}

if __name__ == '__main__':
    if sys.argv[1] == 'paymentinfo':
        get_payment_info(sys.argv[2], False)