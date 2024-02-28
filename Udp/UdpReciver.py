import socket

# Specify the port number to listen on
RECEIVER_PORT = 6000

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
receiver_socket.bind(('0.0.0.0', RECEIVER_PORT))

print('Receiver is listening...')

# Receive data from senders indefinitely
while True:
    # Receive data and the address of the sender
    data, sender_address = receiver_socket.recvfrom(1024)
    print(f"Received message from {sender_address}: {data.decode('utf-8')}")
