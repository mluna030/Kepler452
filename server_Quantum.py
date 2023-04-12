import socket
import json
from Kepler452.XMSS import random_wmss, sign_mss
import cv2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def pad(data):
    return data + b'\x00' * (16 - len(data) % 16)

def encrypt(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(pad(plain_text)))

# Generate the Winternitz Merkle signature scheme key pair
keypair = random_wmss(4)

# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server is waiting for connections...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Send the public key, Merkle root, and Merkle path to the client
pub_key_data = {'pub': keypair[0].pub, 'merkle_root': keypair[0].merkle_root, 'merkle_path': keypair[0].merkle_path}
client_socket.sendall(json.dumps(pub_key_data).encode())

# Generate a random AES key
aes_key = get_random_bytes(16)

# Send the AES key to the client
client_socket.sendall(aes_key)

# Sign and send the message
message = "Transmitting video..."
signature = sign_mss(keypair, message, 0)
signed_message = {'message': message, 'signature': signature[0]}
encrypted_signed_message = encrypt(json.dumps(signed_message).encode(), aes_key)
client_socket.sendall(encrypted_signed_message)

# Capture video from USB camera
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)

        # Encrypt the frame using AES
        encrypted_frame = encrypt(buffer.tobytes(), aes_key)

        # Send the encrypted frame to the client
        client_socket.sendall(encrypted_frame)

finally:
    cap.release()
    client_socket.close()
    server_socket.close()

