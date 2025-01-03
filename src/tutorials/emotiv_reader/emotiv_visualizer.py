import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import threading
from threading import Event
import hid
from Crypto.Cipher import AES
from emotiv_server import connect_to_device, process_data
from visualize_data import bandpass_filter
from matplotlib.animation import FuncAnimation

class RealtimeEEGVisualizer:
    def __init__(self, buffer_size=1000, num_channels=14):
        self.buffer_size = buffer_size
        self.num_channels = num_channels
        self.data_buffers = [deque(maxlen=buffer_size) for _ in range(num_channels)]
        self.stop_event = Event()
        
        # EEG channel names for Emotiv EPOC+
        self.channel_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 
                            'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
        
        # Initialize the plot with dark theme
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(15, 10))
        self.lines = []
        
        # Adjust these parameters for better visualization
        self.display_window = 500  # Show 500 samples at a time
        self.offset_factor = 50    # Offset between channels for better separation
        self.scale_factor = 0.1    # Scale factor to adjust signal amplitude
        
        # Create color map for different channels
        colors = plt.cm.viridis(np.linspace(0, 1, num_channels))
        
        # Initialize empty lines with proper channel names
        for i in range(num_channels):
            line, = self.ax.plot([], [], 
                               label=self.channel_names[i],
                               color=colors[i],
                               linewidth=0.8)
            self.lines.append(line)
        
        # Customize the plot
        plt.xlabel("Sample Index", fontsize=12, color='white')
        plt.ylabel("EEG Signal (µV)", fontsize=12, color='white')
        plt.title("Real-time EEG Signals", fontsize=14, pad=20, color='white')
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10, 
                  facecolor='black')
        plt.grid(True, alpha=0.3, color='white')
        plt.tight_layout()

        # Initialize the animation
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=50, blit=True)

        self.hid_device = None

    def update_plot(self, frame):
        # Get the current buffer length
        buffer_len = len(self.data_buffers[0])
        
        # Calculate the window start and end
        window_end = buffer_len
        window_start = max(0, window_end - self.display_window)
        
        # Create time index for the window
        x = np.arange(window_start, window_end)
        
        # Update each line with new data
        for i in range(self.num_channels):
            if len(self.data_buffers[i]) > 0:
                # Get data for the current window
                data = np.array(list(self.data_buffers[i]))[-self.display_window:]
                # Convert raw values to microvolts (µV) with adjusted scaling
                scaled_data = (data / 16384.0) * 100 * self.scale_factor
                offset = (self.num_channels - i) * self.offset_factor
                
                # Update line data
                x_window = np.arange(len(scaled_data))
                self.lines[i].set_data(x_window, scaled_data + offset)
        
        # Adjust plot limits to show only the current window
        self.ax.set_xlim(0, self.display_window)
        ymin = -self.offset_factor
        ymax = (self.num_channels + 1) * self.offset_factor
        self.ax.set_ylim(ymin, ymax)
        
        return self.lines

    def add_data(self, channels):
        try:
            # Ensure we have the correct number of channels
            channels = channels[:self.num_channels]
            # Pad with zeros if we have fewer channels than expected
            while len(channels) < self.num_channels:
                channels.append(0)
            
            # Add new data to buffers
            for i, value in enumerate(channels):
                self.data_buffers[i].append(value)
            
        except Exception as e:
            print(f"Error in add_data: {e}")

    def start(self):
        self.data_thread = threading.Thread(target=self.collect_data)
        self.data_thread.daemon = True
        self.data_thread.start()
        plt.show()

    def cleanup(self):
        """Ensure proper cleanup of resources"""
        print("Cleaning up resources...")
        self.stop_event.set()
        if self.hid_device:
            try:
                self.hid_device.close()
                print("Device connection closed.")
            except Exception as e:
                print(f"Error closing device: {e}")
        plt.close('all')

    def collect_data(self):
        try:
            # Connect to the device
            vendor_id, product_id, key = connect_to_device()
            self.hid_device = hid.Device(vendor_id, product_id)
            print("Successfully connected to Emotiv device.")
            
            cipher = AES.new(key.encode(), AES.MODE_ECB)
            
            while not self.stop_event.is_set():
                # Read and process data
                raw_data = self.hid_device.read(32)
                if raw_data:
                    decrypted_data = cipher.decrypt(bytes(raw_data))
                    channels = process_data(decrypted_data)
                    self.add_data(channels)
                
        except KeyboardInterrupt:
            print("\nVisualization stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()

def main():
    visualizer = None
    try:
        visualizer = RealtimeEEGVisualizer()
        print("Starting real-time EEG visualization...")
        print("Press Ctrl+C to stop")
        visualizer.start()
    except KeyboardInterrupt:
        print("\nStopping visualization...")
    finally:
        if visualizer:
            visualizer.cleanup()

if __name__ == "__main__":
    main() 