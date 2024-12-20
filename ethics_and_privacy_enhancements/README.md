# Scenario:
* Person A needs to transfer a sensitive CSV file (containing ID, Name, Email, etc.) securely to Person B over a potentially unsecured network.
* Person A will encode the CSV file locally and then encrypt the decoding key file (ENC file) with a password.
* Person A will share the encoded CSV file and encrypted decoding key (ENC file) over the network into a shared folder.
* Person B will download both the encoded CSV file and encrypted decoding key from the shared folder onto their local machine.
* Person B will decrypt the decoding key file with the same password used by Person A.
* Person B can then use the decrypted key to decode the encoded CSV file back into its original format and store it locally.
* The above repository is the end result of where each file would be located.
* Once the CSV files are no longer needed, both Person A and B should use the data anonymizer to permanently anonymize the CSV files before deleting them.

# Instructions:

## Encrypter (Person A):
* To only have access to the `Data Encrypter` and `Shared` folders.
* Before running the Python script, update the file paths in the script to match your system.
* Run the Python script. This will generate:
  * An encoded CSV file in the `Shared` folder.
  * An encrypted key file (ENC file) in the `Shared` folder for decoding the CSV.

## Decrypter (Person B):
* To only have access to the `Data Decrypter` and `Shared` folders.
* Before running the Python script, update the file paths in the script to match your system.
* Run the Python script. This will:
  * Decrypt the key file (ENC file) using the provided password.
  * Decode the encoded CSV file into its original format.

## Password:
* For demonstration purposes, use the password: DBWL38192@#%
* **Note:** In real-world scenarios, passwords should not be shared openly like this. Consider using a secure method to transmit passwords.

## Anonymizer:
* The anonymizer tool should be used by both Person A and B to anonymize the data for privacy protection once the data is no longer needed.
* Before running the Python script, update the file paths in the script to match your system.
* Running the script will permanently replace and anonymize sensitive data in the CSV file.
