import socket

def receive_file(host, port, filename):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the address
        s.bind((host, port))
        # Listen for incoming connections
        s.listen(1)
        print("Server listening on port", port)
        
        # Resolve the DDNS hostname to get the IP address
        remote_ip = socket.gethostbyname(host)
        
        # Accept a connection
        conn, addr = s.accept()
        print('Connected by', addr)
        
        with conn:
            # Open the file in binary write mode
            with open(filename, 'wb') as f:
                while True:
                    # Receive data from the client
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Write data to the file
                    f.write(data)
            print('File received successfully')

# Define the DDNS hostname and port to listen on
HOST = 'your_ddns_hostname.ddns.net'
PORT = 12345
# Define the filename to save the received file as
FILENAME = 'received_file.txt'

# Call the function to receive the file
receive_file(HOST, PORT, FILENAME)
