import socket
import argparse

def send_message(target_host, target_port, message_text):
    """
    Sends a message to a specified UDP server.

    Args:
        target_host (str): The hostname or IP address of the receiver.
        target_port (int): The port number the receiver is listening on.
        message_text (str): The message to send.
    """
    # Create a UDP socket
    # AF_INET specifies the address family (IPv4)
    # SOCK_DGRAM specifies the socket type (UDP)
    sender_socket = None  # Initialize for the finally block
    try:
        print("Creating UDP socket...")
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP socket created successfully.")

        # Resolve the receiver's hostname to get its IP address (if a hostname is provided)
        # For UDP, this resolution happens before sending, or `sendto` can do it implicitly
        # but explicit resolution provides better error handling for hostname issues.
        print(f"Resolving hostname '{target_host}' if necessary...")
        # Note: gethostbyname is used here for clarity, but sendto can resolve too.
        # If target_host is already an IP, gethostbyname will just return it.
        receiver_ip = socket.gethostbyname(target_host)
        print(f"Target address resolved to: {receiver_ip}:{target_port}")

        # Encode the message string to bytes
        message_bytes = message_text.encode('utf-8')

        # Send the message to the receiver
        print(f"Sending message '{message_text}' to {receiver_ip}:{target_port}...")
        sender_socket.sendto(message_bytes, (receiver_ip, target_port))
        print("Message sent successfully.")

    except socket.gaierror as e:
        print(f"Error: Hostname resolution failed for '{target_host}'. {e}")
    except socket.error as e:
        print(f"Error: Socket error during sending. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the socket is closed if it was created
        if sender_socket:
            print("Closing socket.")
            sender_socket.close()

def main():
    """
    Parses command-line arguments and initiates sending the UDP message.
    """
    parser = argparse.ArgumentParser(description="UDP Message Sender")
    parser.add_argument("--host", help="Receiver's hostname or IP address", required=True)
    parser.add_argument("--port", type=int, default=6000,
                        help="Receiver's port number (default: 6000)")
    parser.add_argument("--message", help="The message string to send", required=True)

    args = parser.parse_args()

    send_message(args.host, args.port, args.message)

if __name__ == "__main__":
    main()
