import numpy as np
import os
import time
import argparse
from bit import Key
from pprint import pprint

# Try to import cupy, fall back to numpy if not available
try:
    import cupy as cp

    gpu_enabled = True
except ImportError:
    gpu_enabled = False

# Load CSV file into a list
def load_csv_to_list(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return data


# Generate a Bitcoin address and return relevant information
def generate_bitcoin_info():
    key = Key()
    return {
        'address': key.address,
        'private_key': key.to_wif(),
        'public_key': key.public_key.hex(),
        'segwit_address': key.segwit_address
    }


# Function to check if the string is in the array
def check_string_in_array(string, array):
    if gpu_enabled:
        # Transfer the array to GPU memory if GPU is enabled
        gpu_array = cp.array(array, dtype=object)
        # Check if the string exists in the GPU array
        return cp.any(gpu_array == string)
    else:
        # Check if the string exists in the CPU array
        return np.any(np.array(array) == string)


# Stress test function
def stress_test(array, duration):
    start_time = time.time()
    count = 0

    while time.time() - start_time < duration:
        bitcoin_info = generate_bitcoin_info()
        check_string_in_array(bitcoin_info['address'], array)
        count += 1

    print(f"Stress test completed. Total addresses checked: {count}")


# Main function
def main():
    parser = argparse.ArgumentParser(description='Bitcoin Address Checker')
    parser.add_argument('--stress-test', type=int, help='Run stress test for specified seconds')
    args = parser.parse_args()

    file_path = 'data.txt'  # Replace with the path to your CSV file
    output_file = '/app/output/found_strings.txt'
    array = load_csv_to_list(file_path)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if args.stress_test & int(args.stress_test) != 0:
        stress_test(array, args.stress_test)
    else:
        while True:
            bitcoin_info = generate_bitcoin_info()
            if check_string_in_array(bitcoin_info['address'], array):
                with open(output_file, 'a') as f:
                    f.write(f"Found Bitcoin Address:\n")
                    f.write(f"Address: {bitcoin_info['address']}\n")
                    f.write(f"Private Key: {bitcoin_info['private_key']}\n")
                    f.write(f"Public Key: {bitcoin_info['public_key']}\n")
                    f.write(f"Segwit Address: {bitcoin_info['segwit_address']}\n")
                    f.write("\n")
                print(f"Found: {bitcoin_info['address']}")
            else:
                with open(output_file, 'a') as f:
                    f.write(f"Not Found: {bitcoin_info['address']}")


if __name__ == "__main__":
    main()
