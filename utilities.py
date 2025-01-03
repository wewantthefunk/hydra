import string, random, json, os, time
from jdcal import gcal2jd
from datetime import datetime
from flask_mail import Message, Mail
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import constants

def file_exists(filepath):
    """
    Check if a file exists at the given path.

    :param filepath: The path of the file to be checked.
    :type filepath: str
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(filepath)

def load_json_file(filepath):
    """Read a JSON file and return its contents as a dict."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def send_email(recipients = [], subject = str, body = str, mail = Mail):
    msg = Message(subject, sender='admin@hydra.com', recipients=recipients)
    msg.body = body
    mail.send(msg)
    return "Email sent!"

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

def date_to_julian(date):
    # Get the current date
    now = datetime.now()

    tt = now.timetuple() 

    jd = int('%d%03d' % (tt.tm_year, tt.tm_yday))

    return jd

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def load_private_key():
    print('utilities loading private key')
    if file_exists('private/private.pem'):
        print('found the key file')
        with open("private/private.pem", "rb") as f:
            constants.PRIVATE_KEY = serialization.load_pem_private_key(
                f.read(),
                password=None,  # If the key is encrypted, provide the password here. Otherwise, use `None`.
                backend=default_backend()
            )
    else:
        print("can't find the key file")

    print('------------')

def load_mail_server_info():
    if file_exists('private/mail.json'):
        mailInfo = load_json_file('private/mail.json')
        return mailInfo
    
def use_encrypt(v: str) -> bool:
    if v == '1':
        return True
    
    return False

def str_to_bool(s: str):
    if s.lower().strip() == "true" or s.lower().strip() == '1':
        return True
    elif s.lower().strip() == "false" or s.lower().strip() == '0':
        return False
    else:
        raise ValueError("Invalid boolean string")
    
def create_base40_string():
    # Get the current time in seconds since Unix epoch (1970-01-01)
    current_time = int(time.time())

    # Convert the number of milliseconds to base 40 representation
    base40_chars = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
    base40_string = ""

    while current_time > 0:
        # Get the remainder of the division by 40 and use it as an index for base40_chars
        index = current_time % 40
        base40_string = base40_chars[index] + base40_string

        # Divide the number by 40 to prepare for the next iteration
        current_time //= 40

    # Pad the resulting string with leading zeros if necessary to make it 20 characters long
    base40_string = base40_string.zfill(20)

    result = ""

    for letter in base40_string:
        if letter == '0':
            result = result + get_random_letter()
        else:
            result = result + letter

    return result

def get_random_letter():
    # Get all lowercase and uppercase letters in the English alphabet
    letters = string.ascii_letters

    # Use the random.choice() function to select a random letter from the list
    random_letter = random.choice(letters)

    return random_letter

if __name__ == '__main__':
    print(create_base40_string())