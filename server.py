from socket import *
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import threading

# RSA and AES utilities
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

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

# Server setup
serverPort = 12000  # Ensure this matches the client connection port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(5)

print("Server is ready to receive connections")

clients = []
keys = {}  # Map client sockets to their keys

# Generate RSA keys for the server
private_key, public_key = generate_rsa_keys()

# Function to handle a single client
def handle_client(client_socket):
    try:
        # Send the public RSA key to the client
        client_socket.send(public_key.export_key())

        # Receive the encrypted AES key from the client
        encrypted_key = client_socket.recv(2048)
        aes_key = rsa_decrypt(private_key, encrypted_key)

        # Store the AES key for the client
        keys[client_socket] = aes_key
        
        while True:
            # Receive encrypted message from client
            data = client_socket.recv(1024)
            if not data:
                break

            # Show encrypted message
            print(f"Encrypted message received: {data.hex()}")

            # Decrypt the message
            decrypted_message = aes_decrypt(data, aes_key)
            print(f"Decrypted message: {decrypted_message}")
            
            # Create a response and encrypt it for all clients using the AES key of the sender
            response = f"Server response to: {decrypted_message}"
            encrypted_response = aes_encrypt(response, aes_key)
            
            # Send the encrypted response to all clients
            for client in clients:
                client.send(encrypted_response)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        keys.pop(client_socket, None)
        print("Client disconnected")

# Accepting multiple clients
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"New connection from {addr}")
    clients.append(connectionSocket)
    threading.Thread(target=handle_client, args=(connectionSocket,)).start()