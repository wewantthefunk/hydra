import sqlite3
from typing import List
import constants, utilities
from datetime import date


class User:
    def __init__(self, email, username, id, user_type, passphrase, is_verified=False, verification_code='000000', is_active=True):
        self.email = email
        self.username = username
        self.id = id
        self.user_type = user_type
        self.passphrase = passphrase
        self.is_verified = is_verified
        self.verification_code = verification_code
        self.is_active = is_active

class Session:
    def __init__(self, username, token, issued, id):
        self.username = username
        self.token = token
        self.issued = issued
        self.id = id

class Event:
    def __init__(self, id, name, startdate, enddate, starttime, endtime, location, inviteonly, invitecode, max, allowanonymoussignups, requiresignin, sku, relationship, last_cancel, organizer_as_attendee, cost = 0.0, price_id = '', paymentRequired = 0, currentattendees = 0):
        self.id = id
        self.name = name
        self.start_date = startdate
        self.end_date = enddate
        self.start_time = starttime
        self.end_time = endtime
        self.location = location
        self.invite_only = inviteonly
        self.invite_code = invitecode
        self.max_attendees = max
        self.current_attendees = currentattendees
        self.allow_anonymous_signups = allowanonymoussignups
        self.require_signin = requiresignin
        self.payment_required = paymentRequired
        self.cost = cost
        self.sku = sku
        self.relationship = relationship
        self.last_cancel = last_cancel
        self.organizer_as_attendee = organizer_as_attendee
        self.price_id = price_id

class Attendee:
    def __init__(self, name, email, uniqueId, userType, badgeNumber, receiptUrl):
        self.name = name
        self.email = email
        self.uniqueId = uniqueId
        self.userType = userType
        self.badgeNumber = badgeNumber
        self.recieptUrl = receiptUrl

def get_all_users() -> List[User]:
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users ORDER BY username")

    # Fetch all the rows
    rows = CURSOR.fetchall()

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def get_user(uname: str) -> List[User]:
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users where username = '" + uname + "'")

    # Fetch all the rows
    rows = CURSOR.fetchall()

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def get_user(uname: str) -> List[User]:
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users where username = '" + uname + "'")

    # Fetch all the rows
    rows = CURSOR.fetchall()

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def get_user_by_userid(userid: int) -> List[User]:
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users  WHERE id = '" + str(userid) + "'")
    rows = CURSOR.fetchall()

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def update_user_verification_code(email: str, vcode: str) -> bool:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("UPDATE users SET verificationCode = '" + vcode + "' WHERE email = '" + email + "'")
    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def create_user_session(jdate: int, uname: str, token: str) -> bool:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate) + " OR username = '" + uname + "'")
    conn.commit()
    CURSOR.execute("INSERT INTO session (token, username, issued) VALUES ('" + token + "','" + uname + "'," + str(jdate) + ")")
    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def update_token(token: str, uname: str) -> bool:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("UPDATE session SET token = '" + token + "' WHERE username = '" + uname + "'")
    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def get_user_by_email_or_username(email: str, username: str) -> List[User]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE email = '" + email + "' OR username = '" + username +  "'")
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def get_user_by_email(email: str) -> List[User]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE email = '" + email + "'")
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def get_user_by_email_and_verification_code(email: str, code: str) -> List[User]:
    result = []
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE email = '" + email + "' AND verificationCode = '" + code + "'")
    rows = CURSOR.fetchall()

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)
    
    CURSOR.close()
    conn.close()

    return result

def get_session_by_username_token_and_issued(jdate: int, uname: str, token: str) -> List[Session]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate))
    conn.commit()

    urows = get_user_by_email_or_username(uname, uname)

    if len(urows) < 1:
        return []
    
    uname = urows[0].username

    # Retrieve all users
    CURSOR.execute("SELECT * FROM session WHERE (username = '" + uname + "' OR username = '" + urows[0].email + "') AND token = '" + token + "' AND issued = " + str(jdate))
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        rs = get_user(uname)
        if len(rs) > 0:
            session = Session(row[constants.SESSION_USER_NAME_COL], 
                        row[constants.SESSION_TOKEN_COL], 
                        row[constants.SESSION_ISSUED_COL],
                        rs[0].id
                    )
            result.append(session)

    CURSOR.close()
    conn.close()

    return result

def create_account(username: str, passphrase: str, email: str, vcode: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive, uniqueId) VALUES ('" + username + "', '" + passphrase + "','" + email + "', 99, 0,'" + vcode + "',1,'" + utilities.create_base40_string() + "')")
    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def check_admin(username: str) -> List[User]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE isActive = 1 AND (usertype = " + str(constants.ADMIN_USER) + ' OR usertype = ' + str(constants.SUPER_USER) + ") AND (username = '" + username + "' OR email = '" + username + "')")
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def check_organizer(username: str) -> List[User]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE isActive = 1 AND (usertype = " + str(constants.ADMIN_USER) + ' OR usertype = ' + str(constants.SUPER_USER) + ' OR usertype = ' + str(constants.ORGANIZER) + ") AND (username = '" + username + "' OR email = '" + username + "')")
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        user = User(row[constants.USER_EMAIL_COL], 
                    row[constants.USER_NAME_COL], 
                    row[constants.USER_ID_COL], 
                    row[constants.USER_TYPE_COL],
                    row[constants.USER_PASSPHRASE_COL],
                    row[constants.USER_IS_VERIFIED_COL],
                    row[constants.USER_VERIFICATION_CODE_COL],
                    row[constants.USER_IS_ACTIVE_COL]
                   )
        result.append(user)

    CURSOR.close()
    conn.close()

    return result

def verify_account(id: int, passphrase: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    CURSOR.execute("UPDATE users SET isVerified = " + str(constants.VERIFIED_ACCOUNT) + " WHERE id = " + str(id))
    conn.commit()

    CURSOR.close()
    conn.close()

    return {'message': 'Account Verified', 'result': constants.RESULT_OK}

def unverify_user(id: int) -> bool:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    CURSOR.execute("UPDATE users SET isVerified = " + str(constants.UNVERIFIED_ACCOUNT) + " WHERE id = " + str(id))
    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def get_event_by_userid_and_name_or_invite_code(userId: int, name: str, code: str) -> Event:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']

    result = Event(-1, '', '', '', '', '', '', 0, '', 0, 0, 0, '', 0, '', 0, 0, '', 0)

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("SELECT * FROM events WHERE code = '" + code + "'")
    r = CURSOR.fetchall()

    found = False

    if len(r) > 0:
        price_id = ''
            
        for price in prices:
            if price['sku'] == r[0][constants.EVENT_SKU_COL]:
                price_id = price['price_id']

        result = Event(r[0][constants.EVENT_ID_COL], 
                       r[0][constants.EVENT_NAME_COL], 
                       r[0][constants.EVENT_START_DATE_COL], 
                       r[0][constants.EVENT_END_DATE_COL], 
                       r[0][constants.EVENT_START_TIME_COL], 
                       r[0][constants.EVENT_END_TIME_COL], 
                       r[0][constants.EVENT_LOCATION_COL], 
                       r[0][constants.EVENT_INVITE_TYPE_COL], 
                       r[0][constants.EVENT_INVITE_CODE_COL], 
                       r[0][constants.EVENT_MAX_ATTENDEES_COL], 
                       r[0][constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL], 
                       r[0][constants.EVENT_REQUIRE_SIGNUPS_COL],
                       r[0][constants.EVENT_SKU_COL],
                       constants.EVENT_OWNER,
                       r[0][constants.EVENT_LAST_CANCEL_DATE_COL],
                       r[0][constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                       r[0][constants.EVENT_PAYMENT_COST_COL],
                       price_id,
                       r[0][constants.EVENT_PAYMENT_TYPE_COL],
                       0)
        found = True
    
    if not found:
        CURSOR.execute("SELECT * FROM events WHERE name = '" + name + "'")
        rows = CURSOR.fetchall()

        if len(rows) > 0:
            CURSOR.execute("SELECT * FROM event2owner WHERE ownerId = " + str(userId) + " AND eventId = " + str(rows[0][0]))
            e = CURSOR.fetchall()
            if len(e) > 0:
                result = Event(r[0][constants.EVENT_ID_COL], 
                       r[0][constants.EVENT_NAME_COL], 
                       r[0][constants.EVENT_START_DATE_COL], 
                       r[0][constants.EVENT_END_DATE_COL], 
                       r[0][constants.EVENT_START_TIME_COL], 
                       r[0][constants.EVENT_END_TIME_COL], 
                       r[0][constants.EVENT_LOCATION_COL], 
                       r[0][constants.EVENT_INVITE_TYPE_COL], 
                       r[0][constants.EVENT_INVITE_CODE_COL], 
                       r[0][constants.EVENT_MAX_ATTENDEES_COL], 
                       r[0][constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL], 
                       r[0][constants.EVENT_REQUIRE_SIGNUPS_COL],
                       r[0][constants.EVENT_SKU_COL],
                       constants.EVENT_OWNER,
                       r[0][constants.EVENT_LAST_CANCEL_DATE_COL],
                       r[0][constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                       r[0][constants.EVENT_PAYMENT_COST_COL],
                       price_id,
                       r[0][constants.EVENT_PAYMENT_TYPE_COL])

    CURSOR.close()
    conn.close()

    return result

def create_event(userId: int, name: str, startdate: str, enddate: str, starttime: str, endtime: str, location: str, invite_only: str, max: str, code: str, aas: str, rsi: str, pt: str, co: str, sku: str, last_cancel: str, organizer_as_attendee: str) -> Event:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']

    price_id = ''
            
    for price in prices:
        if price['sku'] == sku:
            price_id = price['price_id']
    
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    sql = "INSERT INTO events (name, startDate, endDate, startTime, endTime, maxAttendees, location, inviteType, code, allowAnonymousSignups, requireSignIn, paymentType, cost, sku, lastCancelDay, organizerAsAttendee, isActive) VALUES('"
    sql = sql + name + "','" + startdate + "','" + enddate + "','" + starttime + "','" + endtime + "'," + max + ",'" + location + "'," + invite_only + ",'" + code + "'," + aas + "," + rsi + "," + pt + "," + co + ",'" + sku + "','" + last_cancel + "'," + str(organizer_as_attendee) + ",1"
    sql = sql + ")"
    CURSOR.execute(sql)
    inserted_id = CURSOR.lastrowid

    CURSOR.execute("INSERT INTO event2owner (eventId, ownerId) VALUES (" + str(inserted_id) + "," + str(userId) + ")")

    conn.commit()

    CURSOR.close()
    conn.close()

    return Event(inserted_id, name, startdate, enddate, starttime, endtime, location, invite_only, code, max, aas, rsi, sku, constants.EVENT_OWNER, last_cancel, organizer_as_attendee, co, price_id, pt, 0)

def update_event(userId: int, name: str, startdate: str, enddate: str, starttime: str, endtime: str, location: str, invite_only: str, max: str, code: str, aas: str, id: int, rsi: str, pt: str, co: str, sku: str, last_cancel: str, organizer_as_attendee: str) -> Event:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    sql = "UPDATE events SET name = '" + name + "',"
    sql = sql + "startDate = '" + startdate + "',"
    sql = sql + "endDate = '" + enddate + "',"
    sql = sql + "startTime = '" + starttime + "',"
    sql = sql + "endTime = '" + endtime + "',"
    sql = sql + "maxAttendees = " + max + ","
    sql = sql + "location = '" + location + "',"
    sql = sql + "inviteType = " + invite_only + ","
    sql = sql + "code = '" + code + "',"
    sql = sql + "allowAnonymousSignups = " + aas + ","
    sql = sql + 'requireSignIn = ' + rsi + ","
    sql = sql + 'paymentType = ' + pt + ","
    sql = sql + 'cost = ' + co + ","
    sql = sql + "sku = '" + sku + "',"
    sql = sql + "lastCancelDay = '" + last_cancel + "',"
    sql = sql + "organizerAsAttendee = " + str(organizer_as_attendee)
    sql = sql + " WHERE id = " + str(id)

    CURSOR.execute(sql)

    conn.commit()

    CURSOR.close()
    conn.close()

    price_id = ''
            
    for price in prices:
        if price['sku'] == sku:
            price_id = price['price_id']

    return Event(id, name, startdate, enddate, starttime, endtime, location, invite_only, code, max, aas, rsi, sku, constants.EVENT_OWNER, last_cancel, organizer_as_attendee, co, price_id, pt)

def get_public_events() -> List[Event]:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']
    
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    

    CURSOR.execute("SELECT * FROM events WHERE isActive = 1 AND endDate > '" + date.today().strftime("%Y-%m-%d") + "' AND inviteType = " + str(constants.PUBLIC_EVENT))
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        price_id = ''
            
        for price in prices:
            if price['sku'] == row[constants.EVENT_SKU_COL]:
                price_id = price['price_id']

        CURSOR.execute("SELECT COUNT(*) FROM attendees WHERE eventId = " + str(row[constants.EVENT_ID_COL]))
        c = CURSOR.fetchall()

        event = Event(row[constants.EVENT_ID_COL],
                     row[constants.EVENT_NAME_COL],
                     row[constants.EVENT_START_DATE_COL],
                     row[constants.EVENT_END_DATE_COL],
                     row[constants.EVENT_START_TIME_COL],
                     row[constants.EVENT_END_TIME_COL],
                     row[constants.EVENT_LOCATION_COL],
                     row[constants.EVENT_INVITE_TYPE_COL],
                     row[constants.EVENT_INVITE_CODE_COL],
                     row[constants.EVENT_MAX_ATTENDEES_COL],
                     row[constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL],
                     row[constants.EVENT_REQUIRE_SIGNUPS_COL],
                     row[constants.EVENT_SKU_COL],
                     constants.EVENT_PUBLIC,
                     row[constants.EVENT_LAST_CANCEL_DATE_COL],
                     row[constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                     row[constants.EVENT_PAYMENT_COST_COL],
                     price_id,
                     row[constants.EVENT_PAYMENT_TYPE_COL],
                     c[0][0]
                     )
        result.append(event)

    CURSOR.close()
    conn.close()

    return result

def get_my_events(user_id: int) -> List[Event]:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']
    
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("SELECT * FROM event2owner WHERE ownerId = " + str(user_id))
    o_rows = CURSOR.fetchall()

    if len(o_rows) > 0:
        ids = ''
        first = True

        for o_row in o_rows:
            if not first:
                ids = ids + ','

            ids = ids + str(o_row[constants.EVENT_OWNER_ID_COL])

            first = False

        # Retrieve all users
        CURSOR.execute("SELECT * FROM events WHERE isActive = 1 AND id in (" + ids + ")")

        rows = CURSOR.fetchall()

        for row in rows:
            price_id = ''
            
            for price in prices:
                if price['sku'] == row[constants.EVENT_SKU_COL]:
                    price_id = price['price_id']

            CURSOR.execute("SELECT COUNT(*) FROM attendees WHERE eventId = " + str(row[constants.EVENT_ID_COL]))
            c = CURSOR.fetchall()

            event = Event(row[constants.EVENT_ID_COL],
                        row[constants.EVENT_NAME_COL],
                        row[constants.EVENT_START_DATE_COL],
                        row[constants.EVENT_END_DATE_COL],
                        row[constants.EVENT_START_TIME_COL],
                        row[constants.EVENT_END_TIME_COL],
                        row[constants.EVENT_LOCATION_COL],
                        row[constants.EVENT_INVITE_TYPE_COL],
                        row[constants.EVENT_INVITE_CODE_COL],
                        row[constants.EVENT_MAX_ATTENDEES_COL],
                        row[constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL],
                        row[constants.EVENT_REQUIRE_SIGNUPS_COL],
                        row[constants.EVENT_SKU_COL],
                        constants.EVENT_OWNER,
                        row[constants.EVENT_LAST_CANCEL_DATE_COL],
                        row[constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                        row[constants.EVENT_PAYMENT_COST_COL],
                        price_id,
                        row[constants.EVENT_PAYMENT_TYPE_COL],
                        c[0][0] + row[constants.EVENT_ORGANIZER_AS_ATTENDEE_COL]
                        )
            result.append(event)

    CURSOR.execute("SELECT * FROM attendees WHERE attending = 1 AND userId = " + str(user_id))
    o_rows = CURSOR.fetchall()

    if len(o_rows) < 1:
        return result
    
    ids = ''
    first = True

    for o_row in o_rows:
        if not first:
            ids = ids + ','

        ids = ids + str(o_row[constants.EVENT_ATTENDEE_ID_COL])

        first = False

    CURSOR.execute("SELECT * FROM events WHERE isActive = 1 AND id in (" + ids + ")")

    rows = CURSOR.fetchall()

    for row in rows:
        price_id = ''
            
        for price in prices:
            if price['sku'] == row[constants.EVENT_SKU_COL]:
                price_id = price['price_id']

        CURSOR.execute("SELECT COUNT(*) FROM attendees WHERE attending = 1 AND eventId = " + str(row[constants.EVENT_ID_COL]))
        c = CURSOR.fetchall()

        event = Event(row[constants.EVENT_ID_COL],
                     row[constants.EVENT_NAME_COL],
                     row[constants.EVENT_START_DATE_COL],
                     row[constants.EVENT_END_DATE_COL],
                     row[constants.EVENT_START_TIME_COL],
                     row[constants.EVENT_END_TIME_COL],
                     row[constants.EVENT_LOCATION_COL],
                     row[constants.EVENT_INVITE_TYPE_COL],
                     row[constants.EVENT_INVITE_CODE_COL],
                     row[constants.EVENT_MAX_ATTENDEES_COL],
                     row[constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL],
                     row[constants.EVENT_REQUIRE_SIGNUPS_COL],
                     row[constants.EVENT_SKU_COL],
                     constants.EVENT_ATTENDEE,
                     row[constants.EVENT_LAST_CANCEL_DATE_COL],
                     row[constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                     row[constants.EVENT_PAYMENT_COST_COL],
                     price_id,
                     row[constants.EVENT_PAYMENT_TYPE_COL],
                     c[0][0]
                     )
        result.append(event)

    CURSOR.close()
    conn.close()

    return result

def get_event(invite: str) -> Event:
    stripe_events = utilities.load_json_file('private/stripe-api-key.json') 
    prices = stripe_events['prices']

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM events WHERE code = '" + invite + "'")
    rows = CURSOR.fetchall()

    result = None

    for row in rows:
        price_id = ''
            
        for price in prices:
            if price['sku'] == row[constants.EVENT_SKU_COL]:
                price_id = price['price_id']

        CURSOR.execute("SELECT COUNT(*) FROM attendees WHERE eventId = " + str(row[constants.EVENT_ID_COL]))
        c = CURSOR.fetchall()

        event = Event(row[constants.EVENT_ID_COL],
                     row[constants.EVENT_NAME_COL],
                     row[constants.EVENT_START_DATE_COL],
                     row[constants.EVENT_END_DATE_COL],
                     row[constants.EVENT_START_TIME_COL],
                     row[constants.EVENT_END_TIME_COL],
                     row[constants.EVENT_LOCATION_COL],
                     row[constants.EVENT_INVITE_TYPE_COL],
                     row[constants.EVENT_INVITE_CODE_COL],
                     row[constants.EVENT_MAX_ATTENDEES_COL],
                     row[constants.EVENT_ALLOW_ANONYMOUS_SIGNUPS_COL],
                     row[constants.EVENT_REQUIRE_SIGNUPS_COL],
                     row[constants.EVENT_SKU_COL],
                     constants.EVENT_OWNER,
                     row[constants.EVENT_LAST_CANCEL_DATE_COL],
                     row[constants.EVENT_ORGANIZER_AS_ATTENDEE_COL],
                     row[constants.EVENT_PAYMENT_COST_COL],
                     price_id,
                     row[constants.EVENT_PAYMENT_TYPE_COL],
                     c[0][0]
                     )
        result = event

    CURSOR.close()
    conn.close()

    return result

def get_event_attendees(invite: str) -> List[Attendee]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM events WHERE code = '" + invite + "'")
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        sql = "select a.badgeNumber, a.receiptUrl, u.username, u.email, u.uniqueId, u.userType from attendees a inner join users u on u.id = a.userId where a.attending = 1 and u.isActive = 1 and a.eventId = " + str(row[constants.EVENT_ID_COL]) + " ORDER BY u.username"
        CURSOR.execute(sql)
        cu = CURSOR.fetchall()

        for c in cu:
            attendee = Attendee(
                            c[2],
                            c[3],
                            c[4],
                            str(c[5]),
                            c[0],
                            c[1]
                        )
            
            result.append(attendee)

    CURSOR.close()
    conn.close()

    return result

def check_in_attendee(badge_number: str, invite: str, check_in_date: str, check_in_time: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    sql = "SELECT a.eventId, a.userId FROM attendees a INNER JOIN events e ON a.eventId = e.id WHERE a.badgeNumber = '" + badge_number + "' AND e.code = '" + invite + "'"
    CURSOR.execute(sql)
    rows = CURSOR.fetchall()

    if len(rows) < 1:
        return False
    
    sql = "INSERT INTO checkin (eventId, checkInDate, checkInTime, attendeeId) VALUES (" + str(rows[0][0]) + ",'" + check_in_date + "','" + check_in_time + "'," + str(rows[0][1]) + ")"

    CURSOR.execute(sql)

    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def delete_event(user_id: int, event_id: int):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    

    sql = "SELECT * FROM event2owner WHERE ownerId = " + str(user_id)
    CURSOR.execute(sql)
    rows = CURSOR.fetchall()

    if len(rows) < 1:
        return False
    
    sql = "UPDATE events SET isActive = 0 WHERE id = " + str(event_id)
    CURSOR.execute(sql)

    conn.commit()

    CURSOR.close()
    conn.close()

    return True

def check_attendance(userid: int, invite: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    sql = "SELECT * FROM events WHERE code = '" + invite + "'"
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) < 1:
        CURSOR.close()
        conn.close()
        return [False, 1]

    event_id = str(c[0][constants.EVENT_ID_COL])

    sql = "SELECT * FROM event2owner WHERE eventId = " + event_id + " AND ownerId = " + str(userid)
    CURSOR.execute(sql)
    c = CURSOR.fetchall()

    if len(c) > 0:
        CURSOR.close()
        conn.close()
        return [False , 2]

    sql = "SELECT * FROM attendees WHERE attending = 1 AND eventId = " + event_id + " AND userId = " + str(userid)
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) > 0:
        CURSOR.close()
        conn.close()
        return [False, 3]

    CURSOR.close()
    conn.close()

    return [True, 0]

def mark_attended(userid: int, invite: str, receipt_id: str, receipt_num: str, receipt_url: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()  

    sql = "SELECT * FROM events WHERE code = '" + invite + "'"
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) < 1:
        CURSOR.close()
        conn.close()
        return [False, '']

    event_id = str(c[0][constants.EVENT_ID_COL])

    sql = "SELECT * FROM attendees WHERE attending = 1 AND eventId = " + event_id + " AND userId = " + str(userid)
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) > 0:
        CURSOR.close()
        conn.close()
        return [True, c[0][3]]
    
    badge_number = utilities.generate_random_string(10, False)
    
    sql = "INSERT INTO attendees (eventId, userId, badgeNumber, receiptId, receiptNum, receiptUrl, attending) VALUES(" + event_id + "," + str(userid) + ",'" + badge_number + "','" + receipt_id + "','" + receipt_num + "','" + receipt_url + "',1)"
    CURSOR.execute(sql)

    conn.commit()

    CURSOR.close()
    conn.close()

    return [True, badge_number]

def mark_skipped(userid: int, invite: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor() 

    sql = "SELECT * FROM events WHERE code = '" + invite + "'"
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) < 1:
        CURSOR.close()
        conn.close()
        return [True, '']

    event_id = str(c[0][constants.EVENT_ID_COL])

    sql = "SELECT * FROM attendees WHERE attending = 1 AND eventId = " + event_id + " AND userId = " + str(userid)
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) < 1:
        CURSOR.close()
        conn.close()
        return [True, '']

    stripe_charge_id = c[0][constants.ATTENDEE_RECEIPT_ID_COL]
    sql = "UPDATE attendees SET attending = 0 WHERE eventId = " + event_id + " AND userId = " + str(userid)
    CURSOR.execute(sql)

    conn.commit()

    CURSOR.close()
    conn.close()

    return [True, stripe_charge_id]

def get_attendance_info(userid: int, invite: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()  

    sql = "SELECT * FROM events WHERE code = '" + invite + "'"
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) < 1:
        CURSOR.close()
        conn.close()
        return [False, '', '']

    event_id = str(c[0][constants.EVENT_ID_COL])

    sql = "SELECT * FROM attendees WHERE attending = 1 AND eventId = " + event_id + " AND userId = " + str(userid)
    CURSOR.execute(sql)

    c = CURSOR.fetchall()

    if len(c) > 0:
        CURSOR.close()
        conn.close()
        return [True, c[0][constants.ATTENDEE_BADGE_NUMBER_COL], 
                      c[0][constants.ATTENDEE_RECEIPT_ID_COL], 
                      c[0][constants.ATTENDEE_RECEIPT_NUM_COL], 
                      c[0][constants.ATTENDEE_RECEIPT_URL_COL]]
    
    CURSOR.close()
    conn.close()
    return [False, '', '']

def update_username(userId: str, new_username: str, passphrase: str, token: str) -> User:
    result = User('', '', 0, constants.ATTENDEE, '', False, '000000', False)

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    sql = "UPDATE users SET username = '" + new_username + "', passphrase = '" + passphrase + "' WHERE id = " +  userId
    CURSOR.execute(sql)

    conn.commit()

    sql = "UPDATE session SET username = '" + new_username + "' WHERE token = '" +  token + "'"
    CURSOR.execute(sql)

    conn.commit()

    c = get_user(new_username)

    if len(c) > 0:
        result = c[0]

    CURSOR.close()
    conn.close()

    return result

def update_email(userId: str, new_email: str, token: str) -> User:
    result = User('', '', 0, constants.ATTENDEE, '', False, '000000', False)

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    sql = "UPDATE users SET email = '" + new_email + "' WHERE id = " +  userId
    CURSOR.execute(sql)

    conn.commit()

    c = get_user_by_email(new_email)

    if len(c) > 0:
        result = c[0]

    CURSOR.close()
    conn.close()

    return result

def update_password(userId: int, new_passphrase: str) -> User:
    result = User('', '', 0, constants.ATTENDEE, '', False, '000000', False)

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    sql = "UPDATE users SET passphrase = '" + new_passphrase + "' WHERE id = " +  str(userId)
    CURSOR.execute(sql)

    conn.commit()

    c = get_user_by_userid(userId)

    if len(c) > 0:
        result = c[0]

    CURSOR.close()
    conn.close()

    return result
