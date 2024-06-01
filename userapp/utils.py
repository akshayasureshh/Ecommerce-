import uuid

def generate_order_id():
    # Generate a UUID (Universally Unique Identifier) and return its hex representation
    return uuid.uuid4().hex[:10]  



from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

# Initialize Fernet cipher suite with the key from settings
cipher_suite = Fernet(settings.FERNET_KEY.encode())


def decrypt_data(encrypted_data):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    except InvalidToken as e:
        # Log or print the exception for debugging purposes
        print(f"Decryption error: {e}")
        raise ValueError('Invalid encrypted data')


# utils.py
from cryptography.fernet import Fernet
from django.conf import settings

cipher_suite = Fernet(settings.FERNET_KEY.encode())

def encrypt_data(data):
    encoded_data = data.encode('utf-8')
    encrypted_data = cipher_suite.encrypt(encoded_data)
    return encrypted_data.decode()
