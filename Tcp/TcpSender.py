import socket
import argparse

def send_file(host, port, filename):
    """
    Connects to a TCP server and sends a specified file.

    Args:
        host (str): The server's hostname or IP address.
        port (int): The port number the server is listening on.
        filename (str): The path to the file to be sent.
    """
    # Create a TCP/IP socket object
    # AF_INET specifies the address family (IPv4)
    # SOCK_STREAM specifies the socket type (TCP)
    try:
        print(f"Attempting to create socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully.")
    except socket.error as e:
        print(f"Error creating socket: {e}")
        return

    try:
        # Resolve the hostname to get the IP address.
        # This is important if a hostname (like a DDNS) is used.
        print(f"Resolving hostname '{host}'...")
        remote_ip = socket.gethostbyname(host)
        print(f"Hostname resolved to IP: {remote_ip}")

        # Connect the socket to the server's address and port
        print(f"Connecting to {remote_ip}:{port}...")
        s.connect((remote_ip, port))
        print(f"Successfully connected to {remote_ip}:{port}.")

        # Open the file in binary read mode ('rb')
        print(f"Opening file '{filename}' for sending...")
        with open(filename, 'rb') as f:
            print(f"Sending file '{filename}'...")
            # Read data from the file in chunks and send it
            while True:
                data = f.read(1024)  # Read 1KB at a time
                if not data:
                    # End of file reached
                    break
                s.sendall(data)  # Send all data in the chunk
            print(f"File '{filename}' sent successfully.")

    except socket.gaierror as e:
        print(f"Error resolving host '{host}': {e}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except socket.error as e:
        print(f"Socket error during connection or sending: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the socket is closed in any case
        print("Closing socket.")
        s.close()

def main():
    """
    Parses command-line arguments and initiates the file sending process.
    """
    parser = argparse.ArgumentParser(description="TCP File Sender")
    parser.add_argument("--host", help="Server's hostname or IP address", required=True)
    parser.add_argument("--port", type=int, default=12345, help="Server's port number (default: 12345)")
    parser.add_argument("--file", help="Path to the file to send", required=True)

    args = parser.parse_args()

    send_file(args.host, args.port, args.file)

if __name__ == "__main__":
    main()
