from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import utilities, constants

def rsa_decrypt(private_key, encrypted_message):
    print(private_key)
    if type(private_key) is type(None):
        utilities.load_private_key()
        private_key = constants.PRIVATE_KEY

    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return decrypted_message.decode('utf-8')