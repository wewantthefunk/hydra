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

def get_user(uname: str) -> List[User]:
    result = []

    conn = sqlite3.connect('data/user_db.db')

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

def create_user_session(jdate: int, uname: str, token: str) -> bool:
    conn = sqlite3.connect('data/user_db.db')

    # Create a cursor object
    CURSOR = conn.cursor()

    CURSOR.execute("DELETE FROM session WHERE issued < " + str(jdate) + " OR username = '" + uname + "'")
    conn.commit()
    CURSOR.execute("INSERT INTO session (token, username, issued) VALUES ('" + token + "','" + uname + "'," + str(jdate) + ")")
    conn.commit()

    conn.close()

    return True