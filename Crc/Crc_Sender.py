# Crc/Crc_Sender.py
#
# Purpose:
# This script demonstrates the sender-side Cyclic Redundancy Check (CRC) calculation.
# CRC is an error-detecting code commonly used in digital networks and storage devices
# to detect accidental changes to raw data.
#
# How it works:
# 1. A generator polynomial (a binary string, e.g., "1011") is agreed upon by sender and receiver.
# 2. The sender appends a number of zero bits (equal to degree of generator, i.e., len(generator)-1)
#    to the end of the original data string.
# 3. This extended data is then divided by the generator polynomial using binary long division (XOR operations).
# 4. The remainder of this division is the CRC checksum.
# 5. The sender transmits the original data followed by the CRC checksum.

def is_binary_string(s):
    """Checks if a string contains only '0's and '1's."""
    return all(c in '01' for c in s)

def validate_generator(g):
    """
    Validates the generator polynomial.
    Checks if it's a binary string and typically starts and ends with '1'.
    """
    if not is_binary_string(g):
        return False
    if len(g) < 2: # Should be at least "11"
        return False
    # Standard CRC generators start and end with '1'.
    # While not strictly required for the algorithm to run, it's a common convention.
    if not g.startswith('1') or not g.endswith('1'):
        print("Warning: Standard generator polynomials usually start and end with '1'.")
        # Allow it for this generic implementation, but warn.
    return True

def calculate_crc(data, generator):
    """
    Calculate CRC checksum for the given data and generator polynomial.
    Args:
        data (str): The binary data string.
        generator (str): The binary generator polynomial string.
    Returns:
        str: The calculated CRC checksum.
    """
    generator_len = len(generator)
    if generator_len == 0:
        raise ValueError("Generator polynomial cannot be empty.")

    # Number of zero bits to append to the data
    num_zeros_to_append = generator_len - 1

    # Append zeros to data for CRC calculation (padding)
    # This effectively multiplies the data by 2^n, where n is the degree of the polynomial.
    working_data = list(data + '0' * num_zeros_to_append)
    working_data_len = len(working_data)

    # Convert generator to a list of ints for XOR operations, if preferred,
    # or keep as string list. Current code uses string list.
    generator_list = list(generator)

    # Perform CRC division (XOR operations)
    # Iterate from the first bit of the data to the point where the generator
    # can no longer fit if aligned with the current bit.
    for i in range(working_data_len - num_zeros_to_append):
        # If the current bit in the working_data (acting as the dividend) is '1',
        # then an XOR operation with the generator is needed at this position.
        if working_data[i] == '1':
            # Perform XOR operation for each bit of the generator
            for j in range(generator_len):
                # XOR the current bit of working_data with the corresponding bit of the generator
                working_data[i + j] = str(int(working_data[i + j]) ^ int(generator_list[j]))

    # The CRC checksum is the remainder of the division, which consists of the last
    # (generator_len - 1) bits of the modified working_data.
    crc_checksum = ''.join(working_data[-(num_zeros_to_append):])
    return crc_checksum

def send_with_crc(data, generator):
    """
    Prepares data with CRC checksum for "sending".
    In this simulation, it just returns the data concatenated with its CRC.
    Args:
        data (str): The original binary data string.
        generator (str): The binary generator polynomial string.
    Returns:
        str: The original data concatenated with the calculated CRC checksum.
    """
    crc_checksum = calculate_crc(data, generator)
    return data + crc_checksum

def main():
    """
    Main function to get user input, calculate CRC, and display results.
    """
    print("--- CRC Sender ---")
    data_input = input("Enter data bits (binary string, e.g., 110101): ")
    generator_input = input("Enter generator polynomial (binary string, e.g., 1011): ")

    if not is_binary_string(data_input):
        print("Error: Data bits must be a binary string (e.g., '110101').")
        return
    if not data_input: # Ensure data is not empty
        print("Error: Data bits cannot be empty.")
        return

    if not validate_generator(generator_input):
        print("Error: Generator polynomial must be a valid binary string (e.g., '1011', typically starting/ending with '1').")
        return
    if len(generator_input) > len(data_input) + (len(generator_input) -1) : # Basic check
        print("Warning: Generator polynomial is unusually long compared to data. Ensure this is intended.")


    print("\n--- Calculating CRC ---")
    try:
        crc_value = calculate_crc(data_input, generator_input)
        transmitted_data = data_input + crc_value

        print(f"Original Data:        {data_input}")
        print(f"Generator Polynomial: {generator_input}")
        print(f"Calculated CRC:       {crc_value}")
        print(f"Transmitted Data:     {transmitted_data}")

    except ValueError as e:
        print(f"Error during CRC calculation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
