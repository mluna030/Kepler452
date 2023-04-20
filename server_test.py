import socket
from Crypto.Cipher import AES
from base64 import b64encode
from Crypto.Random import get_random_bytes

# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5001))
server_socket.listen(5)

print("Server is waiting for connections...")

# Load the image to send
image_file = '/home/pqc452/Downloads/calico.png'
with open(image_file, 'rb') as f:
    image_bytes = f.read()

# Encrypt the image bytes using AES
key = b'secret_key_12345' # Replace with your own secret key
nonce = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(image_bytes)
image_encrypted_bytes = nonce + ciphertext + tag
image_encrypted_base64 = b64encode(image_encrypted_bytes).decode()

# Send the encrypted image to the client
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")
client_socket.sendall(image_encrypted_base64.encode())

# Close the socket server and client
client_socket.close()
server_socket.close()
