from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pandas as pd
import pickle
import base64
import os

# Replace with the path where you stored the trip data
df = pd.read_csv(r"\hypothetical_trip_data.csv")

# Columns to encode
columns_to_encode = ['ID', 'Name', 'Email', 'year', 'major', 'date', 'time']

# Step 1: Encoding the DataFrame and storing mappings
encoding_dict = {}
decoding_dict = {}

for col in columns_to_encode:
    unique_values = df[col].unique()
    encoding_dict[col] = {val: i for i, val in enumerate(unique_values)}
    decoding_dict[col] = {i: val for i, val in enumerate(unique_values)}
    df[col] = df[col].map(encoding_dict[col])

# Step 2: Save the encoded DataFrame to CSV to the 'Shared' folder. Replace the path correspondingly.
encoded_csv_path = r'..\Shared\encoded_data.csv'
df.to_csv(encoded_csv_path, index=False)
print(f"Encoded CSV saved at: {encoded_csv_path}")

# Step 3: Encrypt and save the decoding dictionary
def encrypt_and_save_dict(decoding_dict, password, file_path):
    # Serialize the dictionary with pickle
    dict_bytes = pickle.dumps(decoding_dict)
    
    # Generate a key from the password
    salt = os.urandom(16)  # Store this along with the encrypted file
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    fernet = Fernet(key)

    # Encrypt the serialized dictionary
    encrypted_data = fernet.encrypt(dict_bytes)
    
    # Save salt and encrypted data to a file
    with open(file_path, 'wb') as file:
        file.write(salt + encrypted_data)

    print(f"Decoding dictionary encrypted and saved at: {file_path}")

# Encrypt and save decoding dictionary enc file into the 'Shared' folder. Replace the file path correspondingly.
decrypt_dict_path = r'..\Shared\encrypted_decoding_dict.enc'
# Replace the 2nd parameter with the password you intend to encrypt the above dictionary with.
# This password MUST only be shared to the intended decrypter. The decrypter is NOT supposed to have access to this file.
encrypt_and_save_dict(decoding_dict, 'DBWL38192@#%', decrypt_dict_path)