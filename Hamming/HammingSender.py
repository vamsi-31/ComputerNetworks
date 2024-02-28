# hamming_sender.py

def encode_hamming(data):
    """
    Encode data using Hamming Code.
    """
    # Calculate the number of redundant bits needed (r)
    r = 0
    while 2 ** r < len(data) + r + 1:
        r += 1
    # Initialize the Hamming code
    hamming_code = ['0'] * (len(data) + r)
    # Fill in the data bits
    for i in range(len(hamming_code)):
        if (i + 1) & i != 0:  # Check if i is a power of 2
            hamming_code[i] = data.pop(0)
    # Fill in the redundant bits
    for i in range(r):
        index = 2 ** i - 1
        count = 0
        for j in range(len(hamming_code)):
            if (j + 1) & (index + 1) != 0 and hamming_code[j] == '1':
                count += 1
        if count % 2 == 1:
            hamming_code[index] = '1'
    # Return Hamming code as string
    return ''.join(hamming_code)
