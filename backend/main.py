from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


"""
The code encrypts and decrypts a file.

Note:
Encrypting twice or more will make the decryption irreversible.
"""

# Function to add padding to the content to have a multiple of 16 bytes
def padding(data):
    return data + b"\0" * (16 - len(data) % 16)

# Function to withdraw the padding after decryption
def unpadding(data):
    return data.rstrip(b"\0")


# Directory where the key will be created 
key_folder = 'C:\\Programmation\\vscode\\encrypt_project\\key\\'
os.makedirs(key_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Path where we save the key
key_path = os.path.join(key_folder, 'filekey_aes.key')

def encrypt_file(file_path):
    # Generate an AES key (32 bytes for AES-256)
    key = get_random_bytes(32)

    # Save the key in a secure file
    with open(key_path, 'wb') as file_key:
        file_key.write(key)

    # Read the file to encrypt
    with open(file_path, 'rb') as file:
        original_file = file.read()

    # Add padding to ensure the content is a multiple of 16 bytes
    padded_data = padding(original_file)

    # Generate a random initialization vector (IV) for AES-CBC
    iv = get_random_bytes(16)

    # Create the AES encryption object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    # Save the encrypted data to the file (IV + encrypted data)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_data)

    return True

def decrypt_file(file_path):
    try:
        # Read the key from the file
        with open(key_path, 'rb') as filekey:
            key = filekey.read()

        # Read the encrypted file
        with open(file_path, 'rb') as enc_file:
            encrypted_file = enc_file.read()

        # Separate the IV and the encrypted data
        iv = encrypted_file[:16]
        encrypted_data = encrypted_file[16:]

        # Create the AES decryption object in CBC mode with IV
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt the data
        decrypted_padded_data = cipher.decrypt(encrypted_data)

        # Remove the padding
        decrypted_data = unpadding(decrypted_padded_data)

        # Write the decrypted file
        with open(file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        return True

    except ValueError as e:
        print(f"Decryption error: {e}. The file might not be encrypted properly or at all.")
        return False
