from cryptography.fernet import Fernet

def generate_key():
    """
    Generate a new encryption key.
    """
    return Fernet.generate_key()

def load_key():
    """
    Load the previously generated key.
    """
    return open("secret.key", "rb").read()

def save_key(key):
    """
    Save the generated key to a file.
    """
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_data(data, key):
    """
    Encrypt the data using the provided key.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(data, key):
    """
    Decrypt the data using the provided key.
    """
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()
