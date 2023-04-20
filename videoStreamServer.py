import socket
import json
import cv2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os

# Set up a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5001))
server_socket.listen(5)

print("Server is waiting for connections...")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Start capturing video from the default camera
cap = cv2.VideoCapture(0)

# Loop over the frames and send them to the client
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    #cv2.imshow('frame', frame)
    # Encode the frame in JPEG format
    _, buffer = cv2.imencode('.png', frame)
    #frame_bytes = buffer.tobytes()
    # Get the size of the frame buffer
    size = buffer.nbytes

    # Convert the size to a fixed-length header and send it to the client
    header = size.to_bytes(4, byteorder='big')
    client_socket.send(header)

    # Send the frame buffer to the client
    client_socket.send(buffer)

    # Wait for a key press and stop if the user pressed 'q'
    if cv2.waitKey(1) == ord('q'):
        break
    '''
    # Encode the frame in base64
    frame_base64 = b64encode(framegit_bytes).decode()

    # Send the frame to the client
    client_socket.send(frame_base64.encode())

    # Wait for a key press and stop if the user pressed 'q'
    if cv2.waitKey(1) == ord('q'):
        break'''

# Release the camera and close the sockets
cap.release()
client_socket.close()
server_socket.close()
