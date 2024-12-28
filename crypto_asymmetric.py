from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import utilities

def rsa_decrypt(private_key, encrypted_message):
    if private_key == None:
        private_key = utilities.load_private_key()
        
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return decrypted_message.decode('utf-8')