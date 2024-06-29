import os
import hashlib
import json
import requests
import shutil
import sys
import time

def download_hashes_json(url, output_file):
    """Download the hashes.json file from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    with open(output_file, 'w') as f:
        f.write(response.text)

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
    time.sleep(0.1)
    sys.stdout.write(f"\r[{progress}] {percentage:.2f}%               ")

def verify_and_move_files(hashes_file, directory, outdated_folder, unknown_folder, exclude_folder=".local_storage"):
    """Verify the hashes of files listed in the JSON file and move outdated and unknown ones."""
    with open(hashes_file, 'r') as f:
        file_hashes = json.load(f)

    if not os.path.exists(outdated_folder):
        os.makedirs(outdated_folder)
    if not os.path.exists(unknown_folder):
        os.makedirs(unknown_folder)

    total_files = len(file_hashes)
    scanned_files = 0

    # Track files listed in the hashes.json
    known_files = set(file_hashes.keys())

    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            full_path = os.path.join(directory, relative_path)

            if relative_path.startswith(exclude_folder):
                continue

            if relative_path in known_files:
                actual_hash = calculate_sha256(full_path)
                expected_hash = file_hashes[relative_path]
                if actual_hash != expected_hash:
                    print_progress_bar((scanned_files / total_files) * 100, full_path)
                    print(f"\nFile {full_path} is outdated. Moving to {outdated_folder}.")
                    shutil.move(full_path, os.path.join(outdated_folder, file))
                else:
                    print_progress_bar((scanned_files / total_files) * 100, full_path)
            else:
                print_progress_bar((scanned_files / total_files) * 100, full_path)
                print(f"\nFile {full_path} is unknown. Moving to {unknown_folder}.")
                shutil.move(full_path, os.path.join(unknown_folder, file))

            scanned_files += 1

    # Final update to show 100% completion
    print_progress_bar(100, "")

def main():
    url = "https://raw.githubusercontent.com/Allerek/vibe-rp-cache-cleaner/main/hashes.json"
    hashes_file = "hashes.json"
    outdated_folder = "outdated"
    unknown_folder = "unknown"

    directory = input("Enter the directory to scan: ")

    # Download the hashes.json file
    download_hashes_json(url, hashes_file)
    print(f"Downloaded {hashes_file} from {url}")

    # Verify the files and move outdated and unknown ones
    verify_and_move_files(hashes_file, directory, outdated_folder, unknown_folder)

    print(f"\nChecksums verification complete. Outdated files moved to {outdated_folder}, unknown files moved to {unknown_folder}")

if __name__ == "__main__":
    main()
