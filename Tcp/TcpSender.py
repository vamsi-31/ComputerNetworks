import socket

def send_file(host, port, filename):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Resolve the DDNS hostname to get the IP address
        remote_ip = socket.gethostbyname(host)
        
        # Connect the socket to the server
        s.connect((remote_ip, port))
        
        # Open the file in binary read mode
        with open(filename, 'rb') as f:
            # Read data from the file and send it
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
        print('File sent successfully')

# Define the DDNS hostname of the server
HOST = 'your_ddns_hostname.ddns.net'
PORT = 12345

# Define the filename of the file to send
FILENAME = 'file_to_send.txt'

# Call the function to send the file
send_file(HOST, PORT, FILENAME)
