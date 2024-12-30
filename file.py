import hashlib
import os
import time
import logging

# Configure logging to log changes to a file
logging.basicConfig(filename="file_integrity_log.txt", level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Function to calculate the hash of a file
def calculate_file_hash(file_path, hash_algo='sha256'):
    """Calculate the hash of a file using the specified hashing algorithm."""
    hash_func = hashlib.new(hash_algo)
    
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):  # Read in chunks
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

# Function to monitor files for integrity
def monitor_files(file_paths, interval=10, hash_algo='sha256'):
    """Monitor files for changes by comparing hash values."""
    # Dictionary to store the initial file hashes
    file_hashes = {}
    
    # Calculate and store the initial hashes of the files
    for file_path in file_paths:
        if os.path.exists(file_path):
            file_hashes[file_path] = calculate_file_hash(file_path, hash_algo)
        else:
            print(f"Warning: {file_path} does not exist.")
    
    # Start monitoring the files
    print(f"Monitoring {len(file_paths)} file(s) for changes every {interval} seconds...")
    
    while True:
        time.sleep(interval)  # Wait for the specified interval
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                # Calculate the current hash of the file
                current_hash = calculate_file_hash(file_path, hash_algo)
                
                # Check if the hash has changed
                if current_hash != file_hashes[file_path]:
                    print(f"Change detected in: {file_path}")
                    logging.info(f"Change detected in: {file_path}")
                    file_hashes[file_path] = current_hash  # Update the stored hash
            else:
                print(f"Warning: {file_path} was deleted or moved.")
                logging.warning(f"Warning: {file_path} was deleted or moved.")
        
        print("Monitoring in progress... Press Ctrl+C to stop.")

# Main function to run the script
if __name__ == "__main__":
    # List the files to monitor
    files_to_monitor = ['text1.txt', 'text2.txt']  # Add paths to the files you want to monitor
    
    # Start monitoring the files
    try:
        monitor_files(files_to_monitor, interval=10)  # Monitor every 10 seconds
    except KeyboardInterrupt:
        print("File monitoring stopped.")
