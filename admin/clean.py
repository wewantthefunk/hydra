import os

def delete_file(file_path):
    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Successfully deleted {file_path}")
        except OSError as e:
            print(f"Error deleting file: {e.strerror}")

delete_file('private/private.pem')
delete_file('static/crypto_key.js')
delete_file('data/user_db.db')