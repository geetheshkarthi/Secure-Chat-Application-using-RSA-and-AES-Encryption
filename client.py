from socket import *
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import threading

# RSA and AES utilities
def rsa_encrypt(public_key, data):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(private_key, data):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(data)

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv + ct_bytes  # Append IV to ciphertext for decryption

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted.decode()

# Client setup
serverName = '127.0.0.1'
serverPort = 12000  # Ensure this matches the server listening port
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Receive the server's public RSA key
server_public_key_data = clientSocket.recv(2048)
server_public_key = RSA.import_key(server_public_key_data)

# Generate a unique AES key for the client
aes_key = get_random_bytes(16)

# Encrypt the AES key using the server's public RSA key
encrypted_key = rsa_encrypt(server_public_key, aes_key)
clientSocket.send(encrypted_key)
print("AES key sent to server")

# Function to listen for server messages
def listen_for_messages():
    while True:
        try:
            encrypted_message = clientSocket.recv(1024)
            if not encrypted_message:
                break

            # Show encrypted message
            print(f"Encrypted message received: {encrypted_message.hex()}")

            # Try decrypting the message
            try:
                decrypted_message = aes_decrypt(encrypted_message, aes_key)
                print("From Server:", decrypted_message)
            except:
                print("Received an encrypted message not meant for this client.")
        except Exception as e:
            print(f"Error: {e}")
            break

# Start listening for server messages in a separate thread
threading.Thread(target=listen_for_messages, daemon=True).start()

# Send encrypted messages to the server
while True:
    try:
        message = input("Enter a message: ")
        encrypted_message = aes_encrypt(message, aes_key)
        
        # Show encrypted message
        print(f"Encrypted message sent: {encrypted_message.hex()}")
        
        clientSocket.send(encrypted_message)
    except Exception as e:
        print(f"Error: {e}")
        break