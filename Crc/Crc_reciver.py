# crc_receiver.py

def verify_crc(received_data, generator):
    """
    Verify CRC checksum for the received data.
    """
    # Convert received data and generator to lists for easier manipulation
    received_data = list(received_data)
    generator = list(generator)
    # Perform CRC division
    for i in range(len(received_data) - (len(generator) - 1)):
        if received_data[i] == '1':
            for j in range(len(generator)):
                received_data[i + j] = str(int(received_data[i + j]) ^ int(generator[j]))
    # If any non-zero remainder is found, error detected
    for bit in received_data[-(len(generator) - 1):]:
        if bit == '1':
            return False
    return True
