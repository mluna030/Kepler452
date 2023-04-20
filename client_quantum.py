import socket
import json
from XMSS import verify_mss
import cv2
import numpy as np
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

def unpad(data):
    return data.rstrip(b'\x00')

def decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(b64decode(cipher_text)))

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.1', 5000))

# Receive the public key, Merkle root, and Merkle path from the server
pub_key_data = json.loads(client_socket.recv(4096).decode())

# Receive the AES key from the server
aes_key = client_socket.recv(16)

# Receive the encrypted signed message from the server
encrypted_signed_message = client_socket.recv(4096)
signed_message = json.loads(decrypt(encrypted_signed_message, aes_key).decode())
message = signed_message['message']
signature = signed_message['signature']

# Verify the signature
verified = verify_mss(signature, pub_key_data['pub'], message, 0)

if verified:
    print("The message is valid:", message)
else:
    print("The message is not valid")

# Create a window to display the video stream
cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)

try:
    while True:
        # Receive the encrypted video frame from the server
        encrypted_frame = client_socket.recv(8192)

        # Decrypt the video frame using AES
        decrypted_frame = decrypt(encrypted_frame, aes_key)

        # Convert the decrypted frame bytes to an image
        img_array = np.frombuffer(decrypted_frame, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('Video Stream', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    client_socket.close()
