from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import utilities

def rsa_decrypt(private_key, encrypted_message):
    print(private_key)
    if type(private_key) is type(None):
        private_key = utilities.load_private_key()
        
    print(private_key)
    if type(private_key) is type(None):
        print("still couldn't load the private key")

    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return decrypted_message.decode('utf-8')