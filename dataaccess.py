import sqlite3
from typing import List
import constants

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
    def __init__(self, username, token, issued):
        self.username = username
        self.token = token
        self.issued = issued

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

    conn.close()

    return result

def get_user_by_email(email: str) -> List[User]:
    result = []

    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users  WHERE email = '" + email + "'")
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

    conn.close()

    return result

def update_user_verification_code(email: str, vcode: str) -> bool:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("UPDATE users SET verificationCode = '" + vcode + "' WHERE email = '" + email + "'")
    conn.commit()

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
    
    conn.close()

    return result

def get_session_by_username_token_and_issued(jdate: int, uname: str, token: str) -> List[Session]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate))
    conn.commit()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM session WHERE username = '" + uname + "' AND token = '" + token + "' AND issued = " + str(jdate))
    rows = CURSOR.fetchall()

    result = []

    for row in rows:
        session = Session(row[constants.SESSION_USER_NAME_COL], 
                    row[constants.SESSION_TOKEN_COL], 
                    row[constants.SESSION_ISSUED_COL]
                   )
        result.append(session)

    conn.close()

    return result

def create_account(username: str, passphrase: str, email: str, vcode: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive) VALUES ('" + username + "', '" + passphrase + "','" + email + "', 99, 0,'" + vcode + "',1)")
    conn.commit()

    conn.close()

    return True

def check_admin(username: str) -> List[User]:
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()

    # Retrieve all users
    CURSOR.execute("SELECT * FROM users WHERE (usertype = " + constants.ADMIN_USER + ' OR usertype = ' + constants.SUPER_USER + ") AND username = '" + username + "'")
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

    conn.close()

    return result

def verify_account(id: int, passphrase: str):
    conn = sqlite3.connect(constants.DB_LOCATION)

    # Create a cursor object
    CURSOR = conn.cursor()    
    
    CURSOR.execute("UPDATE users SET isVerified = " + str(constants.VERIFIED_ACCOUNT) + " WHERE id = " + str(id))
    conn.commit()

    conn.close()

    return {'message': 'Account Verified', 'result': constants.RESULT_OK}