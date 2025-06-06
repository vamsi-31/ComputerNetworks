import textwrap

# CheckSum/CheckSum_Reciver.py
#
# Purpose:
# This script demonstrates the receiver-side checksum verification for error detection.
# It takes a 120-bit binary data word (assumed to be 100 bits of original data + 20 bits of checksum).
# The 100-bit data portion is divided into five 20-bit segments.
# The 20-bit checksum portion is also divided into five 4-bit checksums, one for each data segment.
# For each 20-bit data segment and its corresponding 4-bit received checksum:
# 1. The data segment is further divided into five 4-bit sub-segments.
# 2. These sub-segments are summed using one's complement arithmetic (wrap-around for overflow).
# 3. This sum is then added to the received 4-bit checksum for that segment (again with wrap-around).
# 4. If the result of this final addition is a 4-bit string of all '1's ("1111"),
#    it indicates no error was detected in that segment. Otherwise, an error is assumed.
#
# Note: The original script checked if "1111" - (sum + received_checksum_part) == "0000".
# This is equivalent to checking if (sum + received_checksum_part) == "1111" (after wrap-around).

# --- Constants ---
EXPECTED_TRANSMITTED_LEN = 120 # Expected length of the received binary data (data + checksum)
DATA_LEN = 100                 # Length of the original data part
CHECKSUM_LEN = 20              # Length of the checksum part
SEGMENT_LEN = 20               # Length of each major data segment
SUB_SEGMENT_LEN = 4            # Length of each sub-segment for checksum calculation
# Used for verification: if sum_of_data_sub_segments + received_checksum_part == ALL_ONES_4BIT, then no error.
ALL_ONES_4BIT = "1111"

# Original global variables will be replaced by main_receiver_logic contents
# x = str(input("Enter the 100 Bit Data:")) # Corrected prompt needed for 120 bits
# k = 20 # Replaced by SEGMENT_LEN
# a = 4 # Replaced by SUB_SEGMENT_LEN
# A = [] # Not directly used in receiver in the same way, verification is per segment
# R = x[100:120] # Will be handled by slicing in main_receiver_logic
# i_sum = "1111" # Replaced by ALL_ONES_4BIT for the check condition
# arr = [x[i:i+k] for i in range(0, len(x), k)] # Data segmentation will be in main_receiver_logic

# --- Helper Functions (similar to sender) ---
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

def sum_binary_strings_with_wrap(binary_strings_list, num_bits):
    """
    Sums a list of binary strings with one's complement wrap-around for overflow.
    Args:
        binary_strings_list (list[str]): A list of binary strings.
        num_bits (int): The expected number of bits for each string and the sum.
    Returns:
        str: The binary sum string, with overflow handled by wrap-around,
             padded with leading zeros if necessary.
    """
    current_sum = 0
    for bin_str in binary_strings_list:
        current_sum += int(bin_str, 2)

    sum_bin = bin(current_sum)[2:]

    if len(sum_bin) > num_bits:
        overflow_part = sum_bin[:-num_bits]
        main_part = sum_bin[-num_bits:]
        current_sum = int(main_part, 2) + int(overflow_part, 2)
        sum_bin = bin(current_sum)[2:]

    return sum_bin.zfill(num_bits)

# Renamed from sum_binary_sub_segments_with_wrap to be more generic for receiver's use too.
# And renamed one of its arguments for clarity when used with just two strings.

def verify_received_segment(data_segment, received_segment_checksum, current_sub_segment_len):
    """
    Verifies a single received data segment against its checksum.
    Args:
        data_segment (str): The binary string of the data segment (e.g., 20 bits).
        received_segment_checksum (str): The received checksum for this segment (e.g., 4 bits).
        current_sub_segment_len (int): The length of sub-segments (e.g., 4 bits).
    Returns:
        bool: True if no error detected, False otherwise.
    """
    # Divide the data segment into sub-segments
    sub_segments = textwrap.wrap(data_segment, current_sub_segment_len)

    # Calculate the sum of these data sub-segments
    sum_of_data_sub_segments = sum_binary_strings_with_wrap(sub_segments, current_sub_segment_len)

    # Add this sum to the received checksum for this segment
    # The list contains the sum of data parts and the received checksum part for this segment
    final_check_sum = sum_binary_strings_with_wrap(
        [sum_of_data_sub_segments, received_segment_checksum],
        current_sub_segment_len
    )

    # If the final_check_sum is all '1's (e.g., "1111" for 4-bit), no error detected for this segment.
    # This is because on the sender side, checksum = 1s_complement(sum_of_data).
    # So, on receiver side, sum_of_data + checksum = sum_of_data + 1s_complement(sum_of_data)
    # which should result in all '1's if there are no errors.
    if final_check_sum == ('1' * current_sub_segment_len):
        return True
    else:
        # print(f"    Debug: data_segment={data_segment}, received_checksum={received_segment_checksum}")
        # print(f"    Debug: sum_data_sub_segments={sum_of_data_sub_segments}, final_check_sum={final_check_sum}")
        return False

# --- Main Logic ---
def main_receiver_logic():
    """
    Main logic for the CheckSum Receiver.
    Prompts for transmitted data, separates data and checksum, and verifies each segment.
    """
    transmitted_data_str = input(f"Enter the {EXPECTED_TRANSMITTED_LEN}-bit transmitted data (data + checksum): ")

    if not validate_binary_input(transmitted_data_str, EXPECTED_TRANSMITTED_LEN):
        return

    # Separate the data and the checksum from the transmitted string
    original_data_word = transmitted_data_str[:DATA_LEN]
    received_total_checksum = transmitted_data_str[DATA_LEN:]

    # Divide the data word into its major segments
    data_segments = textwrap.wrap(original_data_word, SEGMENT_LEN)
    # Divide the received total checksum into per-segment checksums
    # Each data segment (20 bits) has a corresponding checksum part (4 bits)
    received_segment_checksums = textwrap.wrap(received_total_checksum, SUB_SEGMENT_LEN)

    print("\n--- Receiver Verification ---")
    all_segments_ok = True
    if len(data_segments) != len(received_segment_checksums):
        print("Error: Mismatch between the number of data segments and checksum segments.")
        print(f"Expected {DATA_LEN // SEGMENT_LEN} of each, but got {len(data_segments)} data segments and {len(received_segment_checksums)} checksum parts.")
        return

    for i in range(len(data_segments)):
        data_segment = data_segments[i]
        checksum_part_for_segment = received_segment_checksums[i]

        # print(f"  Verifying Segment {i+1}/{len(data_segments)}: Data='{data_segment}', Received Checksum Part='{checksum_part_for_segment}'")

        if verify_received_segment(data_segment, checksum_part_for_segment, SUB_SEGMENT_LEN):
            print(f"Segment {i+1}: No error detected.")
        else:
            print(f"Segment {i+1}: Error detected!")
            all_segments_ok = False
            # The original script said "segment is discarded", implying no further processing of it.

    if all_segments_ok:
        print("\nOverall: No errors detected in the received data.")
    else:
        print("\nOverall: Errors were detected in one or more segments.")

if __name__ == "__main__":
    main_receiver_logic()