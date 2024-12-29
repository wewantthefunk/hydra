from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import utilities, constants

def rsa_decrypt(private_key, encrypted_message):
    print('in crypto_asymmetric')
    print(private_key)
    if type(private_key) is type(None):
        print('loading from utilities')
        utilities.load_private_key()
        private_key = constants.PRIVATE_KEY
        
    print(private_key)
    if type(private_key) is type(None):
        print("still couldn't load the private key")

    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return decrypted_message.decode('utf-8')