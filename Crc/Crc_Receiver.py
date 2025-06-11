# Crc/Crc_Receiver.py
#
# Purpose:
# This script demonstrates the receiver-side Cyclic Redundancy Check (CRC) verification.
#
# How it works:
# 1. The receiver uses the same generator polynomial as the sender.
# 2. It takes the received data (which includes the original data + CRC checksum appended by the sender)
#    and divides it by the generator polynomial using binary long division (XOR operations).
# 3. If the remainder of this division is all zeros, the CRC check passes, and it's assumed
#    that no errors occurred during transmission.
# 4. If the remainder is non-zero, an error is detected.

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
    if not g.startswith('1') or not g.endswith('1'):
        print("Warning: Standard generator polynomials usually start and end with '1'.")
    return True

def verify_crc(received_data_str, generator_str):
    """
    Verify CRC checksum for the received data (data + CRC).
    Args:
        received_data_str (str): The complete received binary string (original data + CRC).
        generator_str (str): The binary generator polynomial string.
    Returns:
        bool: True if CRC check passes (remainder is zero), False otherwise.
    """
    generator_len = len(generator_str)
    if generator_len == 0:
        raise ValueError("Generator polynomial cannot be empty.")

    # Convert received data and generator to lists for easier manipulation
    # A copy is made to avoid modifying the original input string if it's passed as a list.
    working_data = list(received_data_str)
    working_data_len = len(working_data)
    generator_list = list(generator_str)

    if working_data_len < generator_len:
        # This case implies the received data is shorter than the generator itself,
        # which means something is wrong, or it's not the data CRC was calculated on.
        # For CRC verification, the remainder would effectively be the data itself if no division steps occur.
        # A more robust check might be needed depending on how "errors" are defined for such short data.
        # Typically, data to be checked is longer than or equal to generator length.
        print("Warning: Received data is shorter than the generator polynomial.")
        # Fall through to the remainder check; if non-zero, it's an error.

    # Perform CRC division (XOR operations)
    # Iterate from the first bit up to the point where the generator can no longer fit.
    # The number of bits in the remainder will be (generator_len - 1).
    # So, the division process goes up to `working_data_len - (generator_len - 1)`.
    for i in range(working_data_len - (generator_len - 1)):
        # If the current bit in working_data is '1', perform XOR with the generator.
        if working_data[i] == '1':
            for j in range(generator_len):
                working_data[i + j] = str(int(working_data[i + j]) ^ int(generator_list[j]))

    # After the division, the remainder is in the last (generator_len - 1) bits of working_data.
    remainder = ''.join(working_data[-(generator_len - 1):])

    # If any bit in the remainder is '1', then the remainder is non-zero, and an error is detected.
    for bit in remainder:
        if bit == '1':
            return False  # Error detected

    return True  # No error detected (remainder is all zeros)

def main():
    """
    Main function to get user input for received data and generator,
    then verify CRC and display the result.
    """
    print("--- CRC Receiver ---")
    received_data_input = input("Enter received data with CRC (binary string, e.g., 110101010): ")
    generator_input = input("Enter generator polynomial (binary string, e.g., 1011): ")

    if not is_binary_string(received_data_input):
        print("Error: Received data must be a binary string.")
        return
    if not received_data_input:
        print("Error: Received data cannot be empty.")
        return

    if not validate_generator(generator_input):
        print("Error: Generator polynomial must be a valid binary string.")
        return

    if len(generator_input) > len(received_data_input):
        print("Error: Generator polynomial cannot be longer than the received data.")
        return

    print("\n--- Verifying CRC ---")
    try:
        crc_ok = verify_crc(received_data_input, generator_input)

        print(f"Received Data:        {received_data_input}")
        print(f"Generator Polynomial: {generator_input}")

        if crc_ok:
            print("Result: CRC check passed. No error detected.")
        else:
            # To show the remainder for educational purposes:
            # This requires re-running a portion of the CRC logic or modifying verify_crc
            # For simplicity, we'll just state error detected.
            # If you wanted to show remainder, verify_crc would need to return it.
            print("Result: CRC check failed. Error detected.")
            # For example, if verify_crc returned the remainder string:
            # remainder_val = verify_crc_and_get_remainder(received_data_input, generator_input)
            # print(f"Calculated Remainder: {remainder_val}")
            # if all(bit == '0' for bit in remainder_val): ... else ...

    except ValueError as e:
        print(f"Error during CRC verification: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
