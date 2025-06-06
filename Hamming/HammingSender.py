# Hamming/HammingSender.py
#
# Purpose:
# This script implements the sender-side of Hamming coding, an error-correcting code
# capable of detecting and correcting single-bit errors.
#
# Hamming Code Generation:
# 1. Determine the number of parity bits (r) required for the given data bits (m).
#    The smallest 'r' is chosen such that 2^r >= m + r + 1.
# 2. The total length of the Hamming code will be n = m + r.
# 3. Parity bits are placed at positions that are powers of 2 (1, 2, 4, 8, ...).
# 4. Data bits are placed in the remaining positions.
# 5. Each parity bit P_k (at position k, where k is a power of 2) is calculated
#    by checking all bit positions 'j' in the code whose binary representation
#    has a '1' in the k-th spot (when k is also seen as a bitmask).
#    For example, P_1 (position 001) checks bits at positions 1, 3, 5, 7, ...
#    P_2 (position 010) checks bits at positions 2, 3, 6, 7, ...
#    P_4 (position 100) checks bits at positions 4, 5, 6, 7, ...
#    The parity bit is set to '0' or '1' to ensure even parity for the bits it covers.

def is_binary_string(s):
    """Checks if a string contains only '0's and '1's."""
    if not s: # Empty string is not a valid binary data input
        return False
    return all(c in '01' for c in s)

def encode_hamming(data_str):
    """
    Encodes a binary data string using Hamming Code.
    Args:
        data_str (str): The binary data string (e.g., "1011").
    Returns:
        str: The generated Hamming code string.
    """
    data_bits = list(data_str) # Convert input string to list of chars
    m = len(data_bits)

    # Calculate the number of parity bits (r)
    r = 0
    while (2**r) < (m + r + 1):
        r += 1

    n = m + r  # Total length of the Hamming code
    hamming_code = ['0'] * n # Initialize with placeholders

    # Place data bits into their correct positions
    # Data bits are placed in positions that are NOT powers of 2.
    # Positions are 1-indexed for power-of-2 calculation, 0-indexed for list access.
    data_idx = 0 # Index for walking through the input data_bits
    for j in range(n):
        position = j + 1 # 1-indexed position
        # Check if 'position' is a power of 2.
        # A number is a power of 2 if it's > 0 and (position & (position - 1)) == 0.
        if (position > 0) and ((position & (position - 1)) == 0):
            # This is a parity bit position, skip for now.
            continue
        else:
            # This is a data bit position.
            if data_idx < m:
                hamming_code[j] = data_bits[data_idx]
                data_idx += 1
            # Else, if data_idx >= m, it means we've placed all data bits.
            # Remaining non-parity positions (if any, due to r calculation) stay '0',
            # though typically m+r is exactly filled by data and calculated parity.

    # Calculate parity bits
    # Iterate for each parity bit P_i at 0-indexed position (2**i - 1)
    for i in range(r):
        parity_pos_0_indexed = (2**i) - 1 # 0-indexed position of this parity bit
        parity_pos_1_indexed = parity_pos_0_indexed + 1 # 1-indexed position

        ones_count = 0
        # Iterate through all bits of the hamming_code (1-indexed 'k_pos')
        for k_pos_0_indexed in range(n):
            k_pos_1_indexed = k_pos_0_indexed + 1

            # Skip the parity bit itself when calculating its own value
            if k_pos_0_indexed == parity_pos_0_indexed:
                continue

            # Check if bit at k_pos_1_indexed is covered by the current parity bit P_i
            # This is true if the i-th bit of k_pos_1_indexed (0-indexed bit from right) is 1
            # e.g., for P_1 (i=0, covers 1,3,5,7...), check if (k_pos_1_indexed >> 0) & 1
            #      for P_2 (i=1, covers 2,3,6,7...), check if (k_pos_1_indexed >> 1) & 1
            if ((k_pos_1_indexed >> i) & 1) == 1:
                if hamming_code[k_pos_0_indexed] == '1':
                    ones_count += 1

        # Set parity bit for even parity
        if ones_count % 2 != 0:
            hamming_code[parity_pos_0_indexed] = '1'
        else:
            hamming_code[parity_pos_0_indexed] = '0'

    return "".join(hamming_code)

def main():
    """
    Main function to get user input, encode it using Hamming code,
    and display the results.
    """
    print("--- Hamming Code Sender ---")
    data_input = input("Enter data bits (binary string, e.g., 101101): ")

    if not is_binary_string(data_input):
        print("Error: Data bits must be a binary string (e.g., '101101').")
        return

    print("\n--- Encoding Data ---")
    try:
        hamming_code_output = encode_hamming(data_input)
        print(f"Original Data:    {data_input}")
        print(f"Generated Hamming Code: {hamming_code_output}")
    except Exception as e:
        print(f"An error occurred during encoding: {e}")

if __name__ == "__main__":
    main()
