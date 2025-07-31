from cryptography.fernet import Fernet
import json
import os
#In a real application, this key would be loaded from a .env or a secure storage like keybase
#For this, we will use a file to store the key and load it, making sure it is the same key used across the application
KEY_FILE = "secret.key"

def load_or_generate_key():
    """Loads the secrete key from a file or generates a new one if it does not exist."""
    if KEY_FILE in globals() and os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key


#Use the same key for the duration of the application
#Same key will be used for encryption and decryption
key = load_or_generate_key()
cipher = Fernet(key)

#Encrypt and decrypt functions used for the logs
def encrypt_log(data: dict) -> bytes:
    """Encrypts a dictionary by first converting it to a JSON string."""
    json_string = json.dumps(data)
    return cipher.encrypt(json_string.encode('utf-8'))

def decrypt_log(token: bytes) -> dict:
    """Decrypts a token back into a dictionary."""
    decrypted_bytes = cipher.decrypt(token)
    return json.loads(decrypted_bytes.decode('utf-8'))