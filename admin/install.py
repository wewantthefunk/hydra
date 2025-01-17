from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization, hashes, padding
import os, sqlite3, random, string, base64, socket, sys

PRIVATE_KEY = None
PUBLIC_KEY = None

def str_to_bool(s: str):
    if s.lower().strip() == "true":
        return True
    elif s.lower().strip() == "false":
        return False
    else:
        raise ValueError("Invalid boolean string")
    
def encrypt(plaintext: str, password: bytes) -> bytes:
    salt = os.urandom(16)  # Generate a random salt for key derivation
    iv = os.urandom(16)  # Generate a random IV for AES-CBC encryption

    # Derive the key from the password and salt using PBKDF2HMAC with SHA-256
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password)

    # Pad the plaintext to match AES-CBC block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Encrypt the padded plaintext using AES-CBC with the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Combine the salt, IV, and ciphertext into a single byte string for storage or transmission
    return salt + iv + ciphertext

def decrypt(ciphertext: bytes, password: bytes) -> str:
    # Extract the salt, IV, and actual ciphertext from the input byte string
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    ciphertext = ciphertext[32:]

    # Derive the key from the password and salt using PBKDF2HMAC with SHA-256
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = kdf.derive(password)

    # Decrypt the ciphertext using AES-CBC with the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted data to remove any padding bytes added during encryption
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    return plaintext.decode()  # Return the decrypted plaintext as a string

def generate_rsa_keys(private_key_length, public_exponent=65537):
    private_key = rsa.generate_private_key(public_exponent, private_key_length)
    public_key = private_key.public_key()

    return private_key, public_key

def rsa_decrypt(private_key, encrypted_message):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return decrypted_message.decode('utf-8')

def rsa_encrypt(public_key, message):
    encrypted_message = public_key.encrypt(message.encode('utf-8'),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return encrypted_message

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def generate_keys():
    global PRIVATE_KEY, PUBLIC_KEY
    # Generate keys with different lengths for public and private keys
    PRIVATE_KEY, PUBLIC_KEY = generate_rsa_keys(4096)  # Adjust key length as needed

def save_keys():
    global PRIVATE_KEY, PUBLIC_KEY
    pk = PUBLIC_KEY.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8').replace("-----BEGIN PUBLIC KEY-----", '').replace("-----END PUBLIC KEY-----",'')

    public_out = 'publicKeyPem = `' + pk.replace("\n", "") + '`;'

    write_to_file('static/crypto_key.js', public_out)

    private_out = PRIVATE_KEY.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')

    write_to_file("private/private.pem", private_out)

def create_sql(passphrase, email, adminName, vcode):
    # Create a connection to the database
    conn = sqlite3.connect('data/user_db.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, passphrase TEXT, email TEXT, usertype INTEGER, isVerified INTEGER, verificationCode TEXT, isActive INTEGER)
    ''')
    
    if passphrase != None:
        # Insert a user
        cursor.execute("INSERT INTO users (username, passphrase, email, usertype, isVerified, verificationCode, isActive) VALUES ('" + adminName + "', '" + passphrase + "','" + email + "', 0, 0,'" + vcode + "',1)")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session
        (username TEXT, token TEXT PRIMARY KEY, issued INTEGER)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events
        (id INTEGER PRIMARY KEY, name TEXT, startDate DATE, endDate DATE, startTime TIME, endTime TIME, maxAttendees INTEGER, location TEXT, inviteType INTEGER, code TEXT)
    ''')

    cursor.execute("PRAGMA table_info(events)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'inviteType' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN inviteType INTEGER")

    if 'code' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN code TEXT")

    if 'allowAnonymousSignups' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN allowAnonymousSignups INTEGER")

    if 'requireSignIn' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN requireSignIn INTEGER")

    if 'paymentType' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN paymentType INTEGER")

    if 'cost' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN cost REAL")

    if 'sku' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN sku TEXT")

    if 'lastCancelDay' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN lastCancelDay DATE")

    if 'organizerAsAttendee' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN organizerAsAttendee INTEGER")

    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'uniqueId' not in columns:
        # Add new column 'code' to the 'events' table if it doesn't exist
        cursor.execute("ALTER TABLE users ADD COLUMN uniqueId TEXT")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendees
        (id INTEGER PRIMARY KEY, userId INTEGER, eventId INTEGER)
    ''')

    cursor.execute("PRAGMA table_info(attendees)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'badgeNumber' not in columns:
        # Add new column 'code' to the 'events' table if it doesn't exist
        cursor.execute("ALTER TABLE attendees ADD COLUMN badgeNumber TEXT")

    if 'receiptId' not in columns:
        # Add new column 'code' to the 'events' table if it doesn't exist
        cursor.execute("ALTER TABLE attendees ADD COLUMN receiptId TEXT")

    if 'receiptNum' not in columns:
        # Add new column 'code' to the 'events' table if it doesn't exist
        cursor.execute("ALTER TABLE attendees ADD COLUMN receiptNum TEXT")

    if 'receiptUrl' not in columns:
        # Add new column 'code' to the 'events' table if it doesn't exist
        cursor.execute("ALTER TABLE attendees ADD COLUMN receiptUrl TEXT")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event2owner
        (id INTEGER PRIMARY KEY, ownerId INTEGER, eventId INTEGER)
    ''')

    # Commit the changes
    conn.commit()

    conn.close()

def generate_random_string(length):
    # Define the characters to choose from for each category
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    special_symbols = "^_-#@"

    # Combine all characters into one string
    all_characters = uppercase_letters + lowercase_letters + numbers + special_symbols

    # Generate the random string using list comprehension and random.choice()
    random_string = ''.join(random.choice(all_characters) for _ in range(length))

    return random_string

def file_exists(filepath):
    """
    Check if a file exists at the given path.

    :param filepath: The path of the file to be checked.
    :type filepath: str
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(filepath)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def execute(is_test_mode: bool):
    passphrase = None
    email = ''
    adminName = ''

    if not file_exists('private/url.json'):
        url = "0.0.0.0"
        use_port = '1'

        url1 = input("Enter the URL for the Hydra server (default " + url + "): ")

        if url1 != '':
            url = url1

        domain_name = input("Enter the Domain Name for the Hydra Server: ")

        use_port1 = input("Should the port be referenced when communicating with users? (1 == yes, 0 == no, default 1): ")

        if use_port1 != '':
            if use_port1 != '1':
                use_port1 = '0'
            
            use_port = use_port1

        write_to_file('private/url.json', '{\n  "url":"' + url + '",\n  "domain":"' + domain_name + '",\n  "use_port":"' + use_port + '"\n}') 

        print("---------------------------")

    if not file_exists('private/port.json'):
        port = ''
        while not isinstance(port, (int)):
            port = input("Enter the port for the Hydra server (default 47863): ")
            if port == '':
                port = 47863

        write_to_file('private/port.json', '{\n  "port":' + str(port) + '\n}')

        print("---------------------------")

    if not file_exists('private/mail.json'):
        print("Configure SMTP Mail Server")
        server = input("Enter server IP address or URL: ")
        port = ''
        while not isinstance(port, (int)):
            port = input("Enter server port (default 587): ")
            if port == '':
                port = 587
        username = input("Enter your mail username: ")
        password = input("Enter your mail password: ")

        write_to_file('private/mail.json', '{\n  "server":"' + server + '",\n  "port":' + str(port) + ',\n  "uname":"' + username + '",\n  "password":"' + password + '"\n}')

        print("---------------------------")

    if not file_exists('static/crypto_key.js') and not file_exists('private/private.pem'):
        print("Configure Your Administrator Login")
        generate_keys()
        save_keys()

        adminName = input("Enter your admin username: ")
        email = input("Enter your administrator email address: ")

        admin_pwd = generate_random_string(25)
        admin_passphrase = 'valid password: ' + adminName

        encrypted = encrypt(admin_passphrase, admin_pwd.encode('utf-8'))

        decrypted = decrypt(encrypted, admin_pwd.encode('utf-8'))

        print("Your admin username is '" + adminName + "'")
        print("THIS IS YOUR ADMIN PASSWORD! COPY IT NOW, AS YOU WILL NOT HAVE ACCESS TO IT AGAIN!")
        print()
        print('   ' + admin_pwd)
        print()
        print('The password cryptography is successful if the following two lines match. If they do not match something is wrong and you should run the clean.sh script and try again!')
        print()
        print(admin_passphrase)
        print(decrypted)

        passphrase = base64.b64encode(encrypted).decode('ascii')
    else:
        print('Passwords already created, skipping')
        print('Building database objects')

    print("---------------------------")

    vcode = generate_random_string(6)

    create_sql(passphrase, email, adminName=adminName, vcode=vcode)

if __name__ == '__main__':
    is_test_mode = False
    if len(sys.argv) > 1:
        is_test_mode = str_to_bool(sys.argv[1])

    print(sys.argv)
    print(is_test_mode)
    execute(is_test_mode=is_test_mode)