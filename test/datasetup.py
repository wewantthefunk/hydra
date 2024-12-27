import base64, random, sqlite3, string
import crypto_symmetric, test_constants

def insert_main_user():
    email = "main@aol.com"
    vcode = "123456"
    admin_pwd = test_constants.MAIN_USER_PASSWORD
    admin_name = test_constants.MAIN_USER_NAME

    admin_passphrase = 'valid password: ' + admin_name

    encrypted = crypto_symmetric.encrypt(admin_passphrase, admin_pwd.encode('utf-8'))
    
    # Create a connection to the database
    conn = sqlite3.connect('test_data/test.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, passphrase TEXT, email TEXT, usertype INTEGER, isVerified INTEGER, verificationCode TEXT, isActive INTEGER)
    ''')

    cursor.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive) VALUES ('" + admin_name + "', '" + base64.b64encode(encrypted).decode('ascii') + "','" + email + "', 0, 1,'" + vcode + "',1)")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session
        (username TEXT, token TEXT PRIMARY KEY, issued INTEGER)
    ''')

    conn.commit()

    conn.close()

    return admin_pwd

def insert_unverified_user():
    email = test_constants.UNVERIFIED_USER_EMAIL
    vcode = test_constants.VERIFICATION_CODE
    admin_pwd = test_constants.UNVERIFIED_USER_PASSWORD
    admin_name = test_constants.UNVERIFIED_USER_NAME

    admin_passphrase = 'valid password: ' + admin_name

    encrypted = crypto_symmetric.encrypt(admin_passphrase, admin_pwd.encode('utf-8'))
    
    # Create a connection to the database
    conn = sqlite3.connect('test_data/test.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, passphrase TEXT, email TEXT, usertype INTEGER, isVerified INTEGER, verificationCode TEXT, isActive INTEGER)
    ''')

    cursor.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive) VALUES ('" + admin_name + "', '" + base64.b64encode(encrypted).decode('ascii') + "','" + email + "', 0, 0,'" + vcode + "',1)")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session
        (username TEXT, token TEXT PRIMARY KEY, issued INTEGER)
    ''')
    
    conn.commit()

    conn.close()

    return admin_pwd

def generate_random_string(length):
    # Define the characters to choose from for each category
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    special_symbols = "^&$%#@!"

    # Combine all characters into one string
    all_characters = uppercase_letters + lowercase_letters + numbers + special_symbols

    # Generate the random string using list comprehension and random.choice()
    random_string = ''.join(random.choice(all_characters) for _ in range(length))

    return random_string

if __name__ == "__main__":
    insert_main_user()
    insert_unverified_user()