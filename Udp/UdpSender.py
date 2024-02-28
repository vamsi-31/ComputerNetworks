import socket

# Receiver's Dynamic DNS hostname
RECEIVER_DDNS_HOSTNAME = 'vamsi.ddns.net'  # Replace with your DDNS hostname
RECEIVER_PORT = 6000

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Prompt the user to enter a message
message = input("Enter message to send: ")

# Resolve the receiver's hostname to get its IP address
receiver_ip = socket.gethostbyname(RECEIVER_DDNS_HOSTNAME)

# Send the message to the receiver
sender_socket.sendto(message.encode('utf-8'), (receiver_ip, RECEIVER_PORT))

print('Message sent to the receiver.')

# Close the socket
sender_socket.close()
