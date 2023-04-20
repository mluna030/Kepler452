import socket
import json
#from XMSS import random_wmss, sign_mss
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

# Send the image to the client
client_socket.send(image_base64.encode())
