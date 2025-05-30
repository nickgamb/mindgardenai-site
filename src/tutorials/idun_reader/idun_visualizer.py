# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Foundational symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
import asyncio
from collections import deque
import matplotlib.pyplot as plt
from bleak import BleakClient, BleakScanner
from threading import Thread
from matplotlib.animation import FuncAnimation

class RealtimeEEGVisualizer:
    def __init__(self, buffer_size=2500, num_channels=1):
        self.buffer_size = buffer_size
        self.num_channels = num_channels
        self.data_buffers = [deque(maxlen=buffer_size) for _ in range(num_channels)]

        # Initialize matplotlib for real-time plotting
        plt.style.use('seaborn-darkgrid')
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.lines = []

        for i in range(num_channels):
            line, = self.ax.plot([], [], label=f"Channel {i+1}")
            self.lines.append(line)

        self.ax.set_xlim(0, buffer_size)
        self.ax.set_ylim(-1000, 1000)  # Adjust as needed based on IDUN device range
        self.ax.legend()
        self.ax.set_title("Real-Time EEG Data")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude")

    def update_plot(self, frame):
        for i, line in enumerate(self.lines):
            line.set_data(range(len(self.data_buffers[i])), list(self.data_buffers[i]))
        return self.lines

    def start(self):
        self.animation = FuncAnimation(self.fig, self.update_plot, interval=50, blit=True)
        plt.show()

    def add_data(self, channel, value):
        self.data_buffers[channel].append(value)

class IDUNEEGDevice:
    DEVICE_NAME_PREFIX = "IGEB"
    SERVICE_UUID = "beffd56c-c915-48f5-930d-4c1feee0fcc3"
    EEG_CHARACTERISTIC_UUID = "beffd56c-c915-48f5-930d-4c1feee0fcc4"

    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.client = None

    async def connect(self):
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name and device.name.startswith(self.DEVICE_NAME_PREFIX):
                print(f"Found device: {device.name}")
                self.client = BleakClient(device.address)
                break

        if not self.client:
            raise Exception("IDUN device not found")

        await self.client.connect()
        print("Connected to IDUN device")

    async def start_stream(self):
        if not self.client:
            raise Exception("Device not connected")

        async def notification_handler(sender, data):
            try:
                # Assuming data comes as two bytes per channel, adjust for actual format
                value = int.from_bytes(data[0:2], byteorder='little', signed=True)
                self.visualizer.add_data(0, value)
            except Exception as e:
                print(f"Error processing data: {e}")

        await self.client.start_notify(self.EEG_CHARACTERISTIC_UUID, notification_handler)
        print("EEG stream started")

    async def stop_stream(self):
        if self.client:
            await self.client.stop_notify(self.EEG_CHARACTERISTIC_UUID)
            print("EEG stream stopped")

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            print("Disconnected from device")

    def run(self):
        loop = asyncio.get_event_loop()

        async def main():
            try:
                await self.connect()
                await self.start_stream()

                # Start visualization in a separate thread
                vis_thread = Thread(target=self.visualizer.start)
                vis_thread.start()

                # Keep running until visualization is closed
                while vis_thread.is_alive():
                    await asyncio.sleep(1)

            except Exception as e:
                print(f"Error: {e}")
            finally:
                await self.stop_stream()
                await self.disconnect()

        loop.run_until_complete(main())

if __name__ == "__main__":
    visualizer = RealtimeEEGVisualizer(buffer_size=2500, num_channels=1)
    device = IDUNEEGDevice(visualizer)
    device.run()


