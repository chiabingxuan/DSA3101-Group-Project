from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pandas as pd
import pickle
import base64
import os

# Configure the function to read in the encoded CSV and ENC file for decryption
def decrypt_and_load_dict(file_path, password):
    with open(file_path, 'rb') as file:
        # Extract salt and encrypted data
        salt = file.read(16)
        encrypted_data = file.read()
    
    # Derive the key using the provided password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    fernet = Fernet(key)
    
    # Decrypt the data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        decoding_dict = pickle.loads(decrypted_data)
        print("Decryption successful. Decoding dictionary loaded.")
        return decoding_dict
    except Exception as e:
        print("Decryption failed. Invalid password.")
        return None

# Retrieve the encoded CSV and ENC file from the 'Shared' folder. Replace the path accordingly.
encoded_csv_path = r'..\Shared\encoded_data.csv'
decrypt_dict_path = r'..\Shared\encrypted_decoding_dict.enc'

# Decoding function using the decrypted dictionary
def decode_csv(encoded_csv_path, decrypt_dict_path):
    # Prompt user for password
    password = input("Enter password to decode: ")
    
    # Decrypt and load the decoding dictionary
    decoding_dict = decrypt_and_load_dict(decrypt_dict_path, password)
    if decoding_dict is None:
        return  # Exit if password is incorrect
    
    # Load the encoded CSV
    encoded_df = pd.read_csv(encoded_csv_path)
    
    # Decode each column based on the decoding dictionary
    for col in decoding_dict:
        encoded_df[col] = encoded_df[col].map(decoding_dict[col])
    
    # Save the decoded DataFrame to a new CSV file. Replace the path accordingly.
    # NO ONE else other than the decrypter can have access to the decoded CSV file.
    decoded_csv_path = r'\decoded_data.csv'
    encoded_df.to_csv(decoded_csv_path, index=False)
    print(f"Decoded CSV saved at: {decoded_csv_path}")

# Call the decode_csv function to test
decode_csv(encoded_csv_path, decrypt_dict_path)