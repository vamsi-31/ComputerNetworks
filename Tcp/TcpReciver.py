import socket
import argparse

def receive_file(host, port, output_filename):
    """
    Listens for an incoming TCP connection and receives a file.

    Args:
        host (str): The hostname or IP address to bind the server to.
                    '0.0.0.0' means listen on all available interfaces.
        port (int): The port number to listen on.
        output_filename (str): The name of the file to save the received data.
    """
    s = None  # Initialize s to None for the finally block
    try:
        # Create a TCP/IP socket object
        # AF_INET specifies the address family (IPv4)
        # SOCK_STREAM specifies the socket type (TCP)
        print(f"Attempting to create socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created successfully.")

        # Bind the socket to the specified host and port
        # The host is the address of the server's network interface
        print(f"Binding server to {host}:{port}...")
        s.bind((host, port))
        print(f"Server bound successfully to {host}:{port}.")

        # Enable the server to accept connections
        # The argument (e.g., 1) is the maximum number of queued connections
        print("Server listening for incoming connections...")
        s.listen(1)
        print(f"Server waiting for a connection on port {port}.")

        # Accept a connection from a client
        # conn is a new socket object usable to send and receive data on the connection
        # addr is the address bound to the socket on the other end of the connection
        conn, addr = s.accept()
        print(f"Connected by {addr}.")

        with conn:
            # Open the specified file in binary write mode ('wb') to save received data
            print(f"Opening file '{output_filename}' for receiving...")
            with open(output_filename, 'wb') as f:
                print(f"Receiving data and writing to '{output_filename}'...")
                # Loop to receive data from the client in chunks
                while True:
                    data = conn.recv(1024)  # Receive up to 1KB of data
                    if not data:
                        # No more data from the client, connection likely closed
                        break
                    f.write(data)  # Write the received data to the file
                print(f"File '{output_filename}' received successfully.")

    except socket.error as e:
        print(f"Socket error: {e}")
    except IOError as e:
        print(f"File I/O error for '{output_filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the main listening socket is closed if it was created
        if s:
            print("Closing server socket.")
            s.close()

def main():
    """
    Parses command-line arguments and starts the TCP file receiver.
    """
    parser = argparse.ArgumentParser(description="TCP File Receiver")
    parser.add_argument("--host", default='0.0.0.0',
                        help="Hostname or IP address to bind the server to (default: '0.0.0.0')")
    parser.add_argument("--port", type=int, default=12345,
                        help="Port number to listen on (default: 12345)")
    parser.add_argument("--output-file", default='received_file.txt',
                        help="Filename to save the received data (default: 'received_file.txt')")

    args = parser.parse_args()

    receive_file(args.host, args.port, args.output_file)

if __name__ == "__main__":
    main()
