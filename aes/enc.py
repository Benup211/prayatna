import boto3
import base64
import secrets  # Import the 'secrets' module for random bytes generation
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# AWS configuration
region = 'ap-south-1'
kms_key_id = 'arn:aws:kms:ap-south-1:660766815990:key/f3101f51-c4a4-4949-b88c-a9d9034b43d3'
encryption_context = {
    'stage': 'youtube',
    'purpose': 'youtube demo',
    'origin': 'us-east-1'
}

# Initialize AWS KMS client
kms = boto3.client('kms', region_name=region)

# AES-256 encryption function
def encrypt_aes(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')

# Generate a random initialization vector (IV)
def generate_random_iv():
    return base64.b64encode(secrets.token_bytes(16)).decode('utf-8')  # Use secrets module for random bytes

# Generate a Data Encryption Key (DEK) using AWS KMS with encryption context
def generate_data_key(key_id, encryption_context):
    response = kms.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256',
        EncryptionContext=encryption_context
    )
    return {
        'plaintext_key': response['Plaintext'],
        'ciphertext_key': response['CiphertextBlob']
    }

# Example usage
def aws_enc(pt):
    try:
        # Simulate known plaintext data (replace with actual data)
        plaintext_data = pt
        print('Plain Data:', plaintext_data)

        # Generate Data Encryption Key (DEK) using AWS KMS with encryption context
        data_key = generate_data_key(kms_key_id, encryption_context)
        dek = data_key['plaintext_key']
        encrypted_data_key = data_key['ciphertext_key']

        # Generate a random initialization vector (IV)
        iv = generate_random_iv()

        # Encrypt data with DEK
        encrypted_data = encrypt_aes(plaintext_data, dek, base64.b64decode(iv))

        # Store encrypted data, DEK, and IV in your database or use them as needed
        # print('Encrypted Data:', encrypted_data)
        # print('Encrypted DEK:', base64.b64encode(encrypted_data_key).decode('utf-8'))
        # print('Initialization Vector:', iv)
        return [encrypted_data,base64.b64encode(encrypted_data_key).decode('utf-8'),iv]
    except Exception as e:
        print('Error:', e)

