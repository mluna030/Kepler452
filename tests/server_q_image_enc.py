import socket
import json
import cv2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os

# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(5)

print("Server is waiting for connections...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Read the image file and encode it in base64
image_file = '/home/pqc452/Downloads/calico.png'
with open(image_file, 'rb') as f:
    image_bytes = f.read()
    image_base64 = b64encode(image_bytes).decode()

# Encrypt the image using AES encryption
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
encrypted_image, tag = cipher.encrypt_and_digest(image_base64.encode('utf-8'))

# Send the encrypted image to the client along with the key and nonce
data = {'key': b64encode(key).decode('utf-8'), 'nonce': b64encode(nonce).decode('utf-8'), 'image': b64encode(encrypted_image).decode('utf-8'), 'tag': b64encode(tag).decode('utf-8')}
json_data = json.dumps(data).encode('utf-8')
client_socket.send(json_data)

# Close the connection
client_socket.close()
server_socket.close()
