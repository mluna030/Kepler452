import socket
import numpy as np
import cv2
from base64 import b64decode

# Set up a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.4', 5001))

cv2.namedWindow('Live Video Feed')

# Loop over the received frames and display them in a window
while True:
    # Receive the frame size header from the server
    header = client_socket.recv(4)

    # If we didn't receive any data, the connection was closed
    if not header:
        break

    # Convert the header to an integer to get the size of the frame buffer
    size = int.from_bytes(header, byteorder='big')

    # Receive the frame buffer from the server
    frame_bytes = b''
    while len(frame_bytes) < size:
        frame_chunk = client_socket.recv(size - len(frame_bytes))
        if not frame_chunk:
            break
        frame_bytes += frame_chunk

    # Convert the bytes to a numpy array
   
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)

    # Decode the frame as an image
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

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
