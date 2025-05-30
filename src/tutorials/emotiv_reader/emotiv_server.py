# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
import hid
import struct
import time
import csv
from Crypto.Cipher import AES
import threading
from threading import Event

# Define the EMOTIV vendor ID and key model (Epoc+)
EMOTIV_VENDOR_ID = 4660
MODEL = 6  # For Epoc+ (Standard)

# Function to generate AES key based on device serial number
def generate_aes_key(serial_number, model):
    """
    Generates an AES key based on the serial number and model.
    """
    if not serial_number or len(serial_number) < 4:
        raise ValueError("Invalid serial number length.")
    
    # Initialize the key list
    k = []
    
    # AES key generation logic based on model
    if model == 2:  # Epoc::Standard
        k = [serial_number[-1], '\0', serial_number[-2], 'T', serial_number[-3], '\x10', serial_number[-4], 'B', serial_number[-1], '\0', serial_number[-2], 'H', serial_number[-3], '\0', serial_number[-4], 'P']
    else:
        # Provide a default key generation logic for other models
        k = [serial_number[-1], serial_number[-2], serial_number[-3], serial_number[-4], 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    
    key = ''.join(k)
    
    # Ensure the key is of appropriate length
    if len(key) not in [16, 24, 32]:
        key = key.ljust(16, '\0')[:16]
    
    return key


# Connect to the EMOTIV device
def connect_to_device():
    """
    Finds and connects to an Emotiv device, retrieves its serial number, 
    and generates the AES key for encryption.
    """
    print("Searching for Emotiv devices...")
    for device in hid.enumerate():
        if device['vendor_id'] == EMOTIV_VENDOR_ID:  # Emotiv vendor ID
            serial_number = device['serial_number']
            print(f"Found device with serial number: {serial_number}")
            
            # Generate AES key based on the serial number and model
            key = generate_aes_key(serial_number, MODEL)
            
            # Return the vendor and product IDs instead of the device object
            return device['vendor_id'], device['product_id'], key
    
    raise RuntimeError("No Emotiv device found.")

# Process EEG data from the device
def process_data(decrypted_data):
    # Split the decrypted data into 2-byte chunks and convert to integers
    channels = [int.from_bytes(decrypted_data[i:i+2], 'big') for i in range(0, len(decrypted_data), 2)]
    return channels

# Save data to CSV file
def save_data_to_csv(data, filename="eeg_data.csv"):
    # Write data to a CSV file
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    print(f"Data saved to {filename}")

def keyboard_listener(stop_event):
    while not stop_event.is_set():
        if input() == 'q':
            print("\nGraceful shutdown initiated...")
            stop_event.set()
            break

# Main function to run the test script
def run():
    hid_device = None
    stop_event = Event()
    
    # Start keyboard listener in separate thread
    keyboard_thread = threading.Thread(target=keyboard_listener, args=(stop_event,))
    keyboard_thread.daemon = True
    keyboard_thread.start()
    
    try:
        # Connect to the device and retrieve vendor_id, product_id, and AES key
        vendor_id, product_id, key = connect_to_device()

        # Open the HID device using the vendor and product IDs
        hid_device = hid.Device(vendor_id, product_id)
        print(f"Successfully opened device.")
        print("Press 'q' and Enter to stop the script gracefully...")

        cipher = AES.new(key.encode(), AES.MODE_ECB)

        while not stop_event.is_set():
            # Read data from the device (32 bytes per packet)
            raw_data = hid_device.read(32)
            if not raw_data:
                print("No data received from device.")
                continue

            # Decrypt the raw data
            decrypted_data = cipher.decrypt(bytes(raw_data))

            # Process the decrypted data
            channels = process_data(decrypted_data)

            # Print and save the data to CSV
            print(f"Channels: {channels}")
            save_data_to_csv(channels)

            # Sleep for a short period to prevent overloading the system
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nTest script stopped by user.")
        stop_event.set()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if hid_device is not None:
            try:
                hid_device.close()
                print("Device connection closed successfully.")
                time.sleep(1)  # Give OS time to release the device
            except Exception as e:
                print(f"Error while closing device: {e}")

if __name__ == "__main__":
    run()
