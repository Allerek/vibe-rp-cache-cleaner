import os
import hashlib
import json
import sys
import time
def calculate_sha256(file_path):
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def print_progress_bar(percentage, file_path, bar_length=40):
    """Print a progress bar in the terminal."""
    block = int(round(bar_length * percentage / 100))
    progress = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\nScanning: {file_path}")
    sys.stdout.flush()
    time.sleep(.1)
    sys.stdout.write(f"\r[{progress}] {percentage:.2f}%")

def get_file_checksums(directory, exclude_files=None):
    """Get SHA256 checksums for all files in a directory except specified ones."""
    if exclude_files is None:
        exclude_files = []

    # Count total files to scan
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    scanned_files = 0

    file_checksums = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file not in exclude_files:
                file_path = os.path.join(root, file)
                file_name = os.path.relpath(file_path, directory)
                
                # Calculate checksum
                file_checksums[file_name] = calculate_sha256(file_path)
                
                # Update and display progress
                scanned_files += 1
                percentage = (scanned_files / total_files) * 100
                print_progress_bar(percentage, file_name)
    
    return file_checksums

def save_checksums_to_json(file_checksums, output_file):
    """Save file checksums to a JSON file with beautified formatting."""
    with open(output_file, 'w') as f:
        json.dump(file_checksums, f, indent=4)

def main():
    directory = input("Enter the directory to scan: ")
    exclude_files = [".local_storage"]
    output_file = "hashes.json"

    file_checksums = get_file_checksums(directory, exclude_files)
    save_checksums_to_json(file_checksums, output_file)
    print(f"\nChecksums saved to {output_file}")

if __name__ == "__main__":
    main()
