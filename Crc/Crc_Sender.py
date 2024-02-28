# crc_sender.py

def calculate_crc(data, generator):
    """
    Calculate CRC checksum for the given data and generator polynomial.
    """
    # Append zeros to data for CRC
    data += '0' * (len(generator) - 1)
    # Convert data and generator to lists for easier manipulation
    data = list(data)
    generator = list(generator)
    # Perform CRC division
    for i in range(len(data) - (len(generator) - 1)):
        if data[i] == '1':
            for j in range(len(generator)):
                data[i + j] = str(int(data[i + j]) ^ int(generator[j]))
    # Return CRC bits
    return ''.join(data[-(len(generator) - 1):])

def send_with_crc(data, generator):
    """
    Send data with CRC checksum.
    """
    # Calculate CRC checksum
    crc_checksum = calculate_crc(data, generator)
    # Return data with CRC checksum
    return data + crc_checksum
