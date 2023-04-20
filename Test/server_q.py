import socket
import json
from XMSS import random_wmss, sign_mss
import cv2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os

def pad(data):
    return data + b'\x00' * (16 - len(data) % 16)

def encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(pad(plain_text)))

# Generate the Winternitz Merkle signature scheme key pair
print("Generating keypair...")
keypair = random_wmss(2)

# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5001))
server_socket.listen(5)

print("Server is waiting for connections...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Send the public key, Merkle root, and Merkle path to the client
pub_key_data = {'pub': keypair[0].pub, 'merkle_root': keypair[0].merkle_root, 'merkle_path': keypair[0].merkle_path}

pub_key_data_json = json.dumps(pub_key_data).encode('utf-8')
print("Server JSON string:", pub_key_data_json)

print("Sending public key data...")
client_socket.sendall(json.dumps(pub_key_data).encode('utf-8'))


# Generate a random AES key
print("Generating AES key...")
aes_key = get_random_bytes(16)

# Send the AES key to the client
print("Sending AES key...")
client_socket.sendall(aes_key)

# Sign and send the message
message = "Transmitting image..."
signature = sign_mss(keypair, message, 0)
signed_message = {'message': message, 'signature': signature[0]}
encrypted_signed_message = encrypt(json.dumps(signed_message).encode('utf-8'), aes_key)
print("Sending encrypted signed message...")
client_socket.sendall(encrypted_signed_message)
print("encrypted signed message sent successfully. ")
# Load the image
image_path = '/home/pqc452/Downloads/calico.png'
if not os.path.isfile(image_path):
    print(f"Error: Image not found at {image_path}")
    client_socket.close()
    server_socket.close()
    exit(1)

image = cv2.imread(image_path)

# Encode the image as PNG
ret, buffer = cv2.imencode('.png', image)

# Encrypt the image using AES
encrypted_image = encrypt(buffer.tobytes(), aes_key)

# Send the encrypted image to the client
print("Sending encrypted image...")
client_socket.sendall(encrypted_image)

print("Image sent successfully.")

client_socket.close()
server_socket.close()
