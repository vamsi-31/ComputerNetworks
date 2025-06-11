import socket
import argparse

def start_server(bind_host, bind_port):
    """
    Starts a UDP server to listen for incoming messages.

    Args:
        bind_host (str): The IP address to bind the server to.
                         '0.0.0.0' means listen on all available network interfaces.
        bind_port (int): The port number to listen on.
    """
    # Create a UDP socket
    # AF_INET specifies the address family (IPv4)
    # SOCK_DGRAM specifies the socket type (UDP)
    # Using a 'with' statement ensures the socket is automatically closed
    # when the block is exited (e.g., on error or KeyboardInterrupt).
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            # Bind the socket to the specified host and port
            # This tells the OS that this script will handle incoming packets for this address/port.
            server_socket.bind((bind_host, bind_port))
            print(f"UDP server listening on {bind_host}:{bind_port}")
            print("Press Ctrl+C to stop the server.")

            # Loop indefinitely to receive data from senders
            while True:
                try:
                    # Receive data and the address of the sender
                    # recvfrom() blocks until a packet is received.
                    # 1024 is the buffer size (max bytes to receive at once).
                    data, sender_address = server_socket.recvfrom(1024)

                    # Decode the received bytes into a string (assuming UTF-8 encoding)
                    message = data.decode('utf-8')
                    print(f"Received message from {sender_address}: {message}")

                except socket.error as e:
                    # Handle potential errors during recvfrom, though less common for UDP
                    print(f"Socket error during receive: {e}")
                except UnicodeDecodeError:
                    print(f"Error decoding message from {sender_address}. Raw data: {data}")

    except socket.error as e:
        print(f"Failed to create or bind socket: {e}")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nServer shutting down due to KeyboardInterrupt.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Server has stopped.")


def main():
    """
    Parses command-line arguments and starts the UDP server.
    """
    parser = argparse.ArgumentParser(description="UDP Message Receiver")
    parser.add_argument("--host", default='0.0.0.0',
                        help="IP address to bind to (default: '0.0.0.0' - listens on all interfaces)")
    parser.add_argument("--port", type=int, default=6000,
                        help="Port number to listen on (default: 6000)")

    args = parser.parse_args()

    start_server(args.host, args.port)

if __name__ == "__main__":
    main()
