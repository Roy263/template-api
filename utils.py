import hashlib
import hmac


def encrypt_password(password,secret):


    # Create an HMAC object with SHA-256
    h = hmac.new(secret_key.encode('utf-8'), password.encode('utf-8'), hashlib.sha256)

    # Get the hexadecimal representation of the hash
    encrypted_password = h.hexdigest()

    print("Encrypted Password (SHA-256):", encrypted_password)

# Your secret key
secret_key = '3VXwz2EaKq7N9jPb'

# Password to hash
password = 'helloWorld!'

encrypt_password(password,secret_key)