from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization, hashes, padding
import os, sqlite3, random, string, base64

PRIVATE_KEY = None
PUBLIC_KEY = None

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

def create_sql(passphrase):
    # Create a connection to the database
    conn = sqlite3.connect('data/user_db.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, passphrase TEXT)
    ''')

    # Insert a user
    cursor.execute("INSERT INTO users (username, passphrase) VALUES ('admin', '" + passphrase + "')")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session
        (username TEXT, token TEXT PRIMARY KEY, issued INTEGER)
    ''')

    # Commit the changes
    conn.commit()

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

generate_keys()
save_keys()

admin_pwd = generate_random_string(25)
admin_passphrase = 'valid password: admin'

encrypted = encrypt(admin_passphrase, admin_pwd.encode('utf-8'))

decrypted = decrypt(encrypted, admin_pwd.encode('utf-8'))

print("Your admin username is 'admin'")
print("THIS IS YOUR ADMIN PASSWORD! COPY IT NOW, AS YOU WILL NOT HAVE ACCESS TO IT AGAIN!")
print('   ' + admin_pwd)
print()
print('The password cryptography is successful if the following two lines match. If they do not match something is wrong and you should run the clean.sh script and try again!')
print()
print(admin_passphrase)
print(decrypted)

create_sql(base64.b64encode(encrypted).decode('ascii'))