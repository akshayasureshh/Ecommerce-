from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()
print(key)  # Print this key and save it securely
