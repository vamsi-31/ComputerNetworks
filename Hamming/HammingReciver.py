# hamming_receiver.py

def decode_hamming(received_data):
    """
    Decode received Hamming code.
    """
    # Calculate the number of redundant bits needed (r)
    r = 0
    while 2 ** r < len(received_data):
        r += 1
    # Initialize the Hamming code
    hamming_code = list(received_data)
    # Check for errors and correct if possible
    error_bit = 0
    for i in range(r):
        index = 2 ** i - 1
        count = 0
        for j in range(len(hamming_code)):
            if (j + 1) & (index + 1) != 0 and hamming_code[j] == '1':
                count += 1
        if count % 2 != 0:
            error_bit += index + 1
    # Correct the error if detected
    if error_bit != 0:
        hamming_code[error_bit - 1] = '1' if hamming_code[error_bit - 1] == '0' else '0'
    # Check if the corrected Hamming code is valid
    for i in range(r):
        index = 2 ** i - 1
        count = 0
        for j in range(len(hamming_code)):
            if (j + 1) & (index + 1) != 0 and hamming_code[j] == '1':
                count += 1
        if count % 2 != 0:
            return False, ''.join(hamming_code)
    return True, ''.join(hamming_code)
