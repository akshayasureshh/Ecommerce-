import uuid

def generate_order_id():
    # Generate a UUID (Universally Unique Identifier) and return its hex representation
    return uuid.uuid4().hex[:10]  

from cryptography.fernet import Fernet

key = b'Yk3Y9mto-hpOCSeqeZLPS8ukt0pS_91vkkUATYHG__U='
cipher_suite = Fernet(key)

def encrypt_data(data):
    try:
        return cipher_suite.encrypt(data.encode()).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(data):
    try:
        return cipher_suite.decrypt(data.encode()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
