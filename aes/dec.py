import boto3
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# AWS configuration
region = 'ap-south-1'
kms_key_id = 'arn:aws:kms:ap-south-1:660766815990:key/f3101f51-c4a4-4949-b88c-a9d9034b43d3'

# Initialize AWS KMS client
kms = boto3.client('kms', region_name=region)

# AES-256 decryption function
def decrypt_aes(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()
    return decrypted.decode('utf-8')

# Decrypt Data Encryption Key (DEK) using AWS KMS with encryption context
def decrypt_data_key(encrypted_data_key, encryption_context):
    response = kms.decrypt(
        CiphertextBlob=base64.b64decode(encrypted_data_key),
        EncryptionContext=encryption_context
    )
    return response['Plaintext']

# Example usage
def aws_dec(cipher,DEK,IV):
    try:
        # Simulate known values (replace with actual values)
        encrypted_data = cipher
        encrypted_data_key =DEK
        iv=IV
        # Sample encryption context used during data key generation
        encryption_context = {
            'stage': 'youtube',
            'purpose': 'youtube demo',
            'origin': 'us-east-1'
        }
        # Decrypt Data Encryption Key (DEK) using AWS KMS with encryption context
        dek = decrypt_data_key(encrypted_data_key, encryption_context)

        # Decrypt the data using DEK
        decrypted_data = decrypt_aes(encrypted_data, dek, base64.b64decode(iv))

        # print('Decrypted Data:', decrypted_data)
        return decrypted_data
    except Exception as e:
        print('Error:', e)
