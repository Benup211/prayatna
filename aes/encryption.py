from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
import secrets
import os
def generate_encryption_key():
    # existing_key = os.getenv("ENCRYPTION_KEY")
    # if existing_key:
    #         print("User exiting key",bytes.fromhex(existing_key))
    #         return bytes.fromhex(existing_key)  # Convert to bytes if needed
    # else:
    #         # Generate a new key
    #         new_key = secrets.token_bytes(32)
            
    #         # Save the new key to the environment variables
    #         os.environ["ENCRYPTION_KEY"] = new_key.hex()
    #         print("New exiting key",new_key)
    #         return new_key
    new_key=b'\x87\x1b\xa4\xd1OH%W\xc7%\xf8\xf7\xed-\\\x1c\xa26\xc0d\xab\x94M`\x0bp\xdd\t\xa9\x85\xf8\xed'
    return new_key
def vectorkey():
    # vec_key=os.getenv("VECTOR_KEY")
    # if vec_key:
    #     print("User vector key",bytes.fromhex(vec_key))
    #     return bytes.fromhex(vec_key)
    # else:
    #      # Generate a new key
    #     vec_key = secrets.token_bytes(16) 
    #     # Save the new key to the environment variables
    #     os.environ["VECTOR_KEY"] = vec_key.hex()
    #     print("New vector key",vec_key)
    #     return vec_key
    vec_key=b'\x0c$Nx\x17\xab\x12\xb5bY@\x122\xd6\xe2E'
    return vec_key
def encrypt_data(data):
    backend = default_backend()
    key=generate_encryption_key()
    iv = vectorkey()
    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return urlsafe_b64encode(iv + ciphertext).decode('utf-8')