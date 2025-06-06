# Network Protocol and Error Control Demonstrations

This project provides Python script implementations of several common networking concepts and error control mechanisms. It's designed for educational purposes to demonstrate how these techniques work at a basic level.

The project includes:
*   **TCP (Transmission Control Protocol) Scripts:** Simple client/server scripts for message/file transfer.
*   **UDP (User Datagram Protocol) Scripts:** Simple client/server scripts for message transfer.
*   **Error Control Algorithms:**
    *   Checksum
    *   CRC (Cyclic Redundancy Check)
    *   Hamming Code (for error detection and correction)

These scripts are standalone demonstrations and are not currently integrated (e.g., CRC is not automatically used by the TCP scripts).

## Project Structure

```
.
├── CheckSum/
│   ├── CheckSum_Sender.py
│   └── CheckSum_Reciver.py
├── Crc/
│   ├── Crc_Sender.py
│   └── Crc_Receiver.py
├── Hamming/
│   ├── HammingSender.py
│   └── Hamming_Receiver.py
├── Tcp/
│   ├── TcpSender.py
│   └── TcpReciver.py
├── Udp/
│   ├── UdpSender.py
│   └── UdpReciver.py
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

*   Python 3.6 or higher is recommended.
*   No external Python packages are required (the `requirements.txt` file is empty).

### Setup and Virtual Environment

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>  # Replace <repository_url> with the actual URL
    cd <repository_directory>
    ```

2.  **Create and activate a Python virtual environment (recommended):**

    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    Using a virtual environment helps manage dependencies and avoids conflicts with global Python packages. While this project has no external dependencies currently, it's good practice.

## Running the Scripts

All scripts are run from the command line using Python.

### 1. TCP Communication

The TCP scripts demonstrate basic file transfer. The receiver starts first, then the sender connects to it.

*   **`Tcp/TcpReciver.py` (TCP Receiver/Server):**
    ```bash
    python Tcp/TcpReciver.py --host <bind_ip> --port <port_number> --output-file <filename_to_save>
    ```
    *   `--host`: IP address for the server to bind to. Use `0.0.0.0` to listen on all available interfaces, or `127.0.0.1` for local testing. (Default: `0.0.0.0`)
    *   `--port`: Port number to listen on. (Default: `12345`)
    *   `--output-file`: Name of the file to save the received data. (Default: `received_file.txt`)

    Example:
    ```bash
    python Tcp/TcpReciver.py --port 9999 --output-file my_received.txt
    ```

*   **`Tcp/TcpSender.py` (TCP Sender/Client):**
    ```bash
    python Tcp/TcpSender.py --host <server_ip> --port <port_number> --file <path_to_file_to_send>
    ```
    *   `--host`: IP address or hostname of the TCP server. For local testing, use `127.0.0.1` if the receiver is on the same machine.
    *   `--port`: Port number the server is listening on. (Default: `12345`)
    *   `--file`: Path to the file you want to send. (Required)

    Example (first create a dummy file `sample.txt`):
    ```bash
    echo "Hello TCP!" > sample.txt
    python Tcp/TcpSender.py --host 127.0.0.1 --port 9999 --file sample.txt
    ```

### 2. UDP Communication

The UDP scripts demonstrate basic message transfer. The receiver starts first.

*   **`Udp/UdpReciver.py` (UDP Receiver):**
    ```bash
    python Udp/UdpReciver.py --host <bind_ip> --port <port_number>
    ```
    *   `--host`: IP address for the receiver to bind to. Use `0.0.0.0` or `127.0.0.1`. (Default: `0.0.0.0`)
    *   `--port`: Port number to listen on. (Default: `6000`)

    Example:
    ```bash
    python Udp/UdpReciver.py --port 7777
    ```

*   **`Udp/UdpSender.py` (UDP Sender):**
    ```bash
    python Udp/UdpSender.py --host <receiver_ip> --port <port_number> --message "<your_message>"
    ```
    *   `--host`: IP address or hostname of the UDP receiver.
    *   `--port`: Port number the receiver is listening on. (Default: `6000`)
    *   `--message`: The message string to send. (Required)

    Example:
    ```bash
    python Udp/UdpSender.py --host 127.0.0.1 --port 7777 --message "Hello UDP!"
    ```

**Note on DDNS for TCP/UDP:** The original scripts mentioned DDNS. If you intend to use these scripts over the internet (not just on your local network or machine), the receiver machine needs to be reachable. This typically involves:
*   Configuring port forwarding on your router if the receiver is behind NAT.
*   Using your public IP address or a DDNS service that points to your public IP.
For local testing, `127.0.0.1` (localhost) is sufficient.

### 3. Checksum Demonstration

These scripts demonstrate a basic checksum algorithm on a fixed-length binary string.

*   **`CheckSum/CheckSum_Sender.py`:**
    Prompts for a 100-bit binary string. Calculates and displays a 20-bit checksum and the data+checksum.
    ```bash
    python CheckSum/CheckSum_Sender.py
    Enter the 100-bit binary data: <100_binary_digits>
    ```

*   **`CheckSum/CheckSum_Reciver.py`:**
    Prompts for a 120-bit binary string (100 bits data + 20 bits checksum). Verifies the checksum for each segment.
    ```bash
    python CheckSum/CheckSum_Reciver.py
    Enter the 120-bit received binary data (data + checksum): <120_binary_digits>
    ```

### 4. CRC (Cyclic Redundancy Check) Demonstration

*   **`Crc/Crc_Sender.py`:**
    Prompts for data bits and a generator polynomial (both binary strings). Shows the calculated CRC and the data to transmit.
    ```bash
    python Crc/Crc_Sender.py
    Enter data bits: 1101011011
    Enter generator polynomial: 1011
    ```

*   **`Crc/Crc_Receiver.py`:**
    Prompts for received data (data + CRC) and the generator polynomial. Reports if errors are detected.
    ```bash
    python Crc/Crc_Receiver.py
    Enter received data with CRC: 1101011011010
    Enter generator polynomial: 1011
    ```
    (Use the "Transmitted Data" from the sender as input here)

### 5. Hamming Code Demonstration

These scripts demonstrate Hamming code for single-bit error detection and correction.

*   **`Hamming/HammingSender.py`:**
    Prompts for data bits (binary string). Shows the generated Hamming code.
    ```bash
    python Hamming/HammingSender.py
    Enter data bits: 1011
    ```

*   **`Hamming/Hamming_Receiver.py`:**
    Prompts for a received Hamming code (binary string). Reports if an error was found, the corrected code, and the extracted original data.
    ```bash
    python Hamming/Hamming_Receiver.py
    Enter received Hamming code: <Hamming_code_from_sender_or_with_an_error>
    ```
    Example (using output from sender `1011` which might be `0110011` for a (7,4) Hamming code, then try changing one bit):
    ```bash
    python Hamming/Hamming_Receiver.py
    Enter received Hamming code: 0110011
    # (No error expected)
    python Hamming/Hamming_Receiver.py
    Enter received Hamming code: 0110111
    # (Error expected and should be corrected)
    ```

## Contributing

Contributions are welcome! If you find issues or have improvements, please feel free to:
1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes and commit them.
4.  Submit a pull request.

## License

This project is for educational purposes. You are free to use, modify, and distribute the code. If no specific license is attached, assume it's available under a permissive license like MIT.
