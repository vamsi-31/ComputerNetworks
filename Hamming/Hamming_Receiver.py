# Hamming/Hamming_Receiver.py
#
# Purpose:
# This script implements the receiver-side of Hamming coding. It takes a received
# Hamming-coded binary string, checks for single-bit errors, corrects them if found,
# and then extracts the original data.
#
# Hamming Code Error Detection and Correction:
# 1. The receiver knows the number of parity bits used (or can deduce it from the total length).
# 2. It recalculates parity for each parity bit position (P_1, P_2, P_4, ...) using the
#    received bits that each parity bit covers.
# 3. If all recalculated parities are correct (e.g., result in an even count of 1s for even parity),
#    no error is detected.
# 4. If some parities are incorrect, the sum of the positions of the incorrect parity bits
#    indicates the position of the erroneous bit in the received code. For example, if P_1 and P_2
#    checks fail, but P_4 is okay, the error is at position 1+2=3.
# 5. If the calculated error position is non-zero, the bit at that position is flipped to correct it.
# 6. After correction (if any), the data bits are extracted from the non-parity positions.

def is_binary_string(s):
    """Checks if a string contains only '0's and '1's."""
    if not s: # Empty string is not a valid Hamming code
        return False
    return all(c in '01' for c in s)

def decode_hamming(received_code_str):
    """
    Decodes a received Hamming code string, detects and corrects single-bit errors,
    and extracts the original data.

    Args:
        received_code_str (str): The received Hamming code string.

    Returns:
        tuple: (extracted_data_str, status_msg, corrected_code_str_or_original)
               - extracted_data_str (str): The extracted original data bits.
               - status_msg (str): A message indicating error status.
               - corrected_code_str_or_original (str): The Hamming code after correction,
                                                       or the original if no error or uncorrectable.
    """
    list_code = list(received_code_str)
    n = len(list_code)

    # Calculate the number of parity bits (r) used in this code length.
    # Smallest 'r' such that 2^r >= n. (e.g., if n=7, r=3; if n=12, r=4)
    r = 0
    while (2**r) < n: # It should be 2^r >= n. If n is a power of 2, 2^r=n is fine.
                      # Example: n=7, r=3 (2^3=8>=7). n=4, r=2 (2^2=4>=4)
        r += 1
    if (2**r) < n : # If 2^r was the condition, then if n is not power of 2, r might be too small.
                    # Correct condition for r based on n:
        r_check = 0
        while True:
            if (2**r_check) >= n:
                r = r_check
                break
            r_check += 1
            if r_check > n: # Safety break for unexpected n values
                return "", "Error: Could not determine parity bit count for n=" + str(n), received_code_str


    # Calculate syndrome (error position)
    # The syndrome bits will indicate the position of the error, if any.
    error_pos = 0
    for i in range(r): # Iterate through each parity bit type (P_1, P_2, P_4 ...)
        parity_check_pos_1_indexed = 2**i # 1-indexed position of the parity bit itself (1, 2, 4, ...)

        ones_count = 0
        # Check all bits covered by this parity bit
        for k_pos_0_indexed in range(n):
            k_pos_1_indexed = k_pos_0_indexed + 1 # 1-indexed position of bit being checked

            # Check if bit at k_pos_1_indexed is covered by parity bit at parity_check_pos_1_indexed
            # This is true if the i-th bit of k_pos_1_indexed is 1
            if ((k_pos_1_indexed >> i) & 1) == 1:
                if list_code[k_pos_0_indexed] == '1':
                    ones_count += 1

        # For even parity, if ones_count is odd, this parity check has failed.
        # Add the position of this parity bit to the error_pos.
        if ones_count % 2 != 0:
            error_pos += parity_check_pos_1_indexed

    # Correct the error
    status_msg = ""
    corrected_code_str = received_code_str # Default to original

    if error_pos > 0 and error_pos <= n:
        # An error was detected at 'error_pos' (1-indexed)
        error_idx_0_indexed = error_pos - 1
        original_bit = list_code[error_idx_0_indexed]
        list_code[error_idx_0_indexed] = '1' if original_bit == '0' else '0'
        status_msg = f"Error detected at position {error_pos}. Bit flipped from {original_bit} to {list_code[error_idx_0_indexed]}."
        corrected_code_str = "".join(list_code)
    elif error_pos == 0:
        status_msg = "No error detected."
        # list_code is already the original, so corrected_code_str is fine
    else: # error_pos > n (should not happen for single correctable errors)
        status_msg = f"Error detected at calculated position {error_pos}, which is out of bounds. Uncorrectable."
        # list_code remains the original received code

    # Extract data bits from the (potentially corrected) code
    extracted_data_list = []
    current_code_to_extract_from = list(corrected_code_str) # Use the corrected version
    for j in range(n):
        position = j + 1 # 1-indexed position
        # Data bits are in positions that are NOT powers of 2
        is_power_of_2 = (position > 0) and ((position & (position - 1)) == 0)
        if not is_power_of_2:
            extracted_data_list.append(current_code_to_extract_from[j])

    return "".join(extracted_data_list), status_msg, corrected_code_str

def main():
    """
    Main function to get user input for received Hamming code,
    decode it, and display results.
    """
    print("--- Hamming Code Receiver ---")
    received_code_input = input("Enter received Hamming code (binary string): ")

    if not is_binary_string(received_code_input):
        print("Error: Received code must be a binary string.")
        return

    print("\n--- Decoding Data ---")
    try:
        extracted_data, status, corrected_code = decode_hamming(received_code_input)

        print(f"Received Code:    {received_code_input}")
        print(f"Status:           {status}")
        if received_code_input != corrected_code : # Only print if different
            print(f"Corrected Code:   {corrected_code}")
        print(f"Extracted Data:   {extracted_data}")

    except Exception as e:
        print(f"An error occurred during decoding: {e}")
        # import traceback
        # traceback.print_exc() # For more detailed debugging if needed

if __name__ == "__main__":
    main()
