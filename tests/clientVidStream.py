import cv2
import socket
import numpy as np

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

# Set the IP address and port to listen on
host = "192.168.0.4"
port = 6666

# Set the dimensions of the video frames
width, height = 320, 240

# Create a window to display the frames
cv2.namedWindow("Video Feed")

# Loop over the frames and display them in a window
while True:
    # Receive the frame from the server
    data, addr = s.recvfrom(65536)
    frame_bytes = np.frombuffer(data, dtype=np.uint8)

    # Decode the frame as an image
    frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)

    # Display the frame
    if frame is not None and frame.size > 0:
        cv2.imshow('Video Feed', frame)
        cv2.waitKey(1)
        print("Received a valid frame with shape:", frame.shape)
    else:
        print('Received an invalid frame')

    # Wait for a key press and stop if the user pressed 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Close the window and the socket
cv2.destroyAllWindows()
s.close()
