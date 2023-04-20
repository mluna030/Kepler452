
import socket
import pickle
import os
import json
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from base64 import b64decode

# Set up a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.4', 5001))

# Set the buffer size to 1 MB
BUFFER_SIZE = 1024 * 1024

cv2.namedWindow('Live Video Feed')

# Loop over the received frames and display them in a window
while True:
    # Receive the frame from the server
    frame_base64 = client_socket.recv(BUFFER_SIZE)

    # If we didn't receive any data, the connection was closed
    if not frame_base64:
        break

    # Decode the frame from base64
    frame_bytes = b64decode(frame_base64)

    # Convert the bytes to a numpy array
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

    # Decode the frame as an image
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    #gray_frame = cv2.cvtColor(frame_array, cv2.COLOR_BGR2GRAY)

    if frame is not None and frame.size > 0:
        cv2.imshow('Live Video Feed', frame)
    else:
        print('Received an invalid frame')


    # Wait for a key press and stop if the user pressed 'q'
    if cv2.waitKey(1) == ord('q'):
        break


# Close the window and the socket
client_socket.close()
cv2.destroyAllWindows()


