import hid
import struct

def list_hid_devices():
    """List all connected HID devices."""
    devices = hid.enumerate()
    for device in devices:
        print(f"Vendor ID: {device['vendor_id']:04x}, Product ID: {device['product_id']:04x}, Manufacturer: {device['manufacturer_string']}, Product: {device['product_string']}")

def open_mouse_device(vendor_id, product_id):
    """Open a HID device by vendor and product ID."""
    try:
        device = hid.Device(vendor_id=vendor_id, product_id=product_id)
        print("Mouse device opened successfully!")
        return device
    except Exception as e:
        print(f"Error opening device: {e}")
        return None

def read_mouse_data(device):
    """Read data from the mouse device."""
    try:
        print("Reading data from mouse. Press Ctrl+C to stop.")
        while True:
            data = device.read(8)  # Adjust the size based on your mouse's report size
            if data:
                print(f"Raw Data: {data}")
                # Example of interpreting basic data (adjust based on your mouse's protocol)
                buttons, x, y = struct.unpack('BBB', bytes(data[:3]))
                print(f"Buttons: {buttons}, X Movement: {x}, Y Movement: {y}")
    except KeyboardInterrupt:
        print("Stopped reading data.")
    except Exception as e:
        print(f"Error reading data: {e}")

def main():
    print("Available HID Devices:")
    list_hid_devices()
    print("\nEnter the Vendor ID and Product ID of your mouse.")
    vendor_id = int(input("Vendor ID (hex): "), 16)
    product_id = int(input("Product ID (hex): "), 16)

    device = open_mouse_device(vendor_id, product_id)
    if device:
        read_mouse_data(device)
        device.close()
        print("Device closed.")

if __name__ == "__main__":
    main()