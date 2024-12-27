from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization, hashes
import os

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