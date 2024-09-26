import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from Flask-CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Temporary folder for uploaded files
UPLOAD_FOLDER = 'C:/Programmation/vscode/encrypt_project/uploads/'
KEY_FOLDER = 'C:/Programmation/vscode/encrypt_project/key/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
os.makedirs(KEY_FOLDER, exist_ok=True)  # Create the key folder if it doesn't exist

# Route for file encryption
@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Generate an AES key
    key = get_random_bytes(32)

    # Save the key to a file
    key_path = os.path.join(KEY_FOLDER, 'filekey_aes.key')
    with open(key_path, 'wb') as file_key:
        file_key.write(key)

    # Read the file and encrypt it
    with open(file_path, 'rb') as original_file:
        original_data = original_file.read()

    # Add PKCS7 padding to the data
    padded_data = pad(original_data, AES.block_size)  # AES.block_size = 16

    # Create an IV and encrypt the data using AES CBC mode
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)

    # Save the encrypted file (IV + encrypted data)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_data)

    return jsonify({'message': 'File encrypted successfully', 'key_file': 'filekey_aes.key'}), 200

# Route for file decryption
@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # Read the AES key from the file
        key_path = os.path.join(KEY_FOLDER, 'filekey_aes.key')
        with open(key_path, 'rb') as key_file:
            key = key_file.read()

        # Read the encrypted file
        with open(file_path, 'rb') as enc_file:
            encrypted_file = enc_file.read()

        # Separate IV and encrypted data
        iv = encrypted_file[:16]
        encrypted_data = encrypted_file[16:]

        # Decrypt the data using AES CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded_data = cipher.decrypt(encrypted_data)

        # Remove PKCS7 padding
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)

        # Write the decrypted data back to the file
        with open(file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        return jsonify({'message': 'File decrypted successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Decryption error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
