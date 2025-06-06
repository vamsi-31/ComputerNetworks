import textwrap

# CheckSum/CheckSum_Sender.py
#
# Purpose:
# This script demonstrates the sender-side checksum calculation for error detection.
# It takes a 100-bit binary data word, divides it into five 20-bit segments.
# For each 20-bit segment, it further divides it into five 4-bit sub-segments.
# A checksum for each 20-bit segment is calculated by:
# 1. Summing its five 4-bit sub-segments using one's complement arithmetic (wrap-around for overflow).
# 2. Taking the one's complement of this 4-bit sum to get the checksum for that segment.
# The final checksum is a 20-bit value, which is the concatenation of the five 4-bit checksums
# (one for each of the original 20-bit segments).
#
# Note: The original script's checksum logic for each segment was a bit unusual.
# It summed the 4-bit sub-segments, then took the one's complement of that sum.
# This refactored version will follow that specific logic.

# --- Constants ---
EXPECTED_DATA_LEN = 100  # Expected length of the input binary data word
SEGMENT_LEN = 20         # Length of each major segment the data word is divided into
SUB_SEGMENT_LEN = 4      # Length of each sub-segment used for checksum calculation within a major segment
# The original script used "1111" to subtract the sum from, which is equivalent to one's complement for 4 bits.
ONES_COMPLEMENT_BASE_4BIT = "1111"

# Original global variables will be replaced by main_sender_logic contents
# x = str(input("Enter the 100 Bit Data:")) # Will be moved into a main function
# k = 20 # Replaced by SEGMENT_LEN
# a = 4 # Replaced by SUB_SEGMENT_LEN
# A = [] # Will be managed within a function
# isum = "1111" # Replaced by ONES_COMPLEMENT_BASE_4BIT
# arr = [x[i:i+k] for i in range(0, len(x), k)] # Will be part of main_sender_logic

# --- Helper Functions ---
def validate_binary_input(data_str, expected_len):
    """
    Validates if the input is a binary string of the expected length.
    Args:
        data_str (str): The input string.
        expected_len (int): The expected length of the string.
    Returns:
        bool: True if valid, False otherwise.
    """
    if len(data_str) != expected_len:
        print(f"Error: Input data must be {expected_len} bits long. You entered {len(data_str)} bits.")
        return False
    if not all(bit in '01' for bit in data_str):
        print("Error: Input data must be a binary string (contain only '0's and '1's).")
        return False
    return True

def calculate_ones_complement(binary_sum, num_bits):
    """
    Calculates the one's complement of a binary string sum.
    This is done by subtracting the sum from a string of all '1's of the same length.
    Args:
        binary_sum (str): The binary sum string (e.g., "0101").
        num_bits (int): The number of bits for the complement (e.g., 4).
    Returns:
        str: The one's complement binary string, padded with leading zeros if necessary.
    """
    base = '1' * num_bits # Uses the global ONES_COMPLEMENT_BASE_4BIT if num_bits is 4
    if num_bits == SUB_SEGMENT_LEN: # More robust to use the constant if appropriate
        base_val = int(ONES_COMPLEMENT_BASE_4BIT, 2)
    else:
        base_val = int(base, 2)

    complement_val = base_val - int(binary_sum, 2)
    complement_bin = bin(complement_val)[2:]
    # Pad with leading zeros to ensure correct length
    return complement_bin.zfill(num_bits)

def sum_binary_sub_segments_with_wrap(sub_segments, num_bits):
    """
    Sums a list of binary sub-segments with one's complement wrap-around for overflow.
    Args:
        sub_segments (list[str]): A list of binary strings (sub-segments).
        num_bits (int): The expected number of bits for each sub-segment and the sum.
    Returns:
        str: The binary sum string, with overflow handled by wrap-around,
             padded with leading zeros if necessary.
    """
    current_sum = 0
    for segment_part in sub_segments: # Renamed 'segment' to 'segment_part' to avoid confusion
        current_sum += int(segment_part, 2)

    # Convert sum to binary string
    sum_bin = bin(current_sum)[2:]

    # Handle one's complement wrap-around if overflow occurs
    if len(sum_bin) > num_bits:
        overflow_part = sum_bin[:-num_bits]
        main_part = sum_bin[-num_bits:]
        # Add the overflow part back to the main part
        current_sum = int(main_part, 2) + int(overflow_part, 2)
        sum_bin = bin(current_sum)[2:] # Recalculate sum_bin

    # Pad with leading zeros to ensure it's `num_bits` long
    return sum_bin.zfill(num_bits)

def generate_segment_checksum(data_segment, current_sub_segment_len): # Renamed sub_segment_len to avoid conflict
    """
    Generates a checksum for a single data segment.
    The segment is divided into sub-segments, which are summed up.
    The one's complement of this sum is the checksum for the segment.
    Args:
        data_segment (str): The binary string of the data segment (e.g., 20 bits).
        current_sub_segment_len (int): The length of sub-segments (e.g., 4 bits).
    Returns:
        str: The calculated checksum for the segment (e.g., 4 bits).
    """
    sub_segments = textwrap.wrap(data_segment, current_sub_segment_len)
    sum_of_sub_segments = sum_binary_sub_segments_with_wrap(sub_segments, current_sub_segment_len)
    segment_checksum = calculate_ones_complement(sum_of_sub_segments, current_sub_segment_len)
    return segment_checksum

# --- Main Logic ---
def main_sender_logic():
    """
    Main logic for the CheckSum Sender.
    Prompts for data, calculates checksum, and prepares data for transmission.
    """
    input_data_str = input(f"Enter the {EXPECTED_DATA_LEN}-bit binary data: ")

    if not validate_binary_input(input_data_str, EXPECTED_DATA_LEN):
        return

    # Divide the input data into major segments
    data_segments = textwrap.wrap(input_data_str, SEGMENT_LEN)

    all_segment_checksums = [] # To store the 4-bit checksum of each 20-bit segment

    # print("\nCalculating checksums per segment...") # Optional: for verbose output
    for i, segment_data in enumerate(data_segments): # Renamed 'segment' to 'segment_data'
        # print(f"  Processing segment {i+1}/{len(data_segments)}: {segment_data}")
        segment_checksum_value = generate_segment_checksum(segment_data, SUB_SEGMENT_LEN)
        all_segment_checksums.append(segment_checksum_value)

    final_checksum_str = "".join(all_segment_checksums)

    print("\n--- Sender Output ---")
    print(f"Original {EXPECTED_DATA_LEN}-bit Data: {input_data_str}")
    # The final checksum is 20 bits (5 segments * 4 bits/segment checksum)
    print(f"Calculated {len(final_checksum_str)}-bit Checksum: {final_checksum_str}")

    transmitted_data_str = input_data_str + final_checksum_str
    print(f"Data to be Transmitted ({len(transmitted_data_str)} bits): {transmitted_data_str}")

if __name__ == "__main__":
    main_sender_logic()