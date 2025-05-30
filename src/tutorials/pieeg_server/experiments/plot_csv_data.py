# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import json
import time

def plot_data(data):
    data = data.astype(float)
    # Map the columns to the expected channel names
    data.columns = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2"]
    
    eeg_data = data.iloc[:, :8]  # The first 8 columns are EEG data
    timestamps = np.arange(len(eeg_data))  # Create a sequence for timestamps

    plt.figure(figsize=(15, 10), facecolor='#333')  # Dark background for the figure
    
    # Define the color mapping
    color_map = {
        "Fp1": "yellow", 
        "Fp2": "orange", 
        "C3": "brown", 
        "C4": "green", 
        "P7": "purple", 
        "P8": "blue", 
        "O1": "grey", 
        "O2": "white"
    }

    ax = plt.gca()
    ax.set_facecolor('#333')  # Dark background for the axes
    ax.tick_params(colors='white')  # White color for the tick labels
    ax.xaxis.label.set_color('white')  # White color for the x-axis label
    ax.yaxis.label.set_color('white')  # White color for the y-axis label
    ax.title.set_color('white')  # White color for the title
    
    for name in data.columns:
        plt.plot(timestamps, data[name], label=name, color=color_map[name], linewidth=0.5, alpha=0.8)
    
    plt.title('EEG Waveforms')
    plt.xlabel('Sample')
    plt.ylabel('Voltage')
    plt.legend(loc='upper right', fontsize='x-small', facecolor='#333', edgecolor='white')  # Dark background for the legend
    plt.grid(True, alpha=0.5, color='white')  # White color for the grid lines
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=plt.gcf().get_facecolor(), edgecolor='none')  # Save with dark background
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path, wait_for_file):
    print("Starting MindGarden data plotting experiment")
    socketio.emit('experiment_update', {
        "message": "Starting MindGarden data plotting experiment",
        "action": "open_file_dialog",
        "fileTypes": [("CSV files", "*.csv"), ("All files", "*.*")]
    })

    # Wait for file selection from frontend
    timeout = 60  # 60 seconds timeout
    if not wait_for_file(timeout):
        print("Timeout waiting for file selection")
        socketio.emit('experiment_error', {"message": "Timeout waiting for file selection"})
        return

    file_path = get_file_path()
    if not file_path:
        print("No file path received")
        socketio.emit('experiment_error', {"message": "No file path received"})
        return

    print(f"File path received: {file_path}")

    try:
        print(f"Reading CSV file: {file_path}")
        eeg_data = pd.read_csv(file_path, header=0)
        
        print(f"Data shape: {eeg_data.shape}")
        socketio.emit('experiment_update', {
            "message": f"Data shape: {eeg_data.shape}",
            "data": eeg_data.head().to_dict()
        })

        # Map the columns to the expected channel names
        eeg_data.columns = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2"]

        print("Generating plot")
        plot_data_base64 = plot_data(eeg_data)
        
        channel_names = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2"]
        stats = {}
        for name in channel_names:
            channel_data = eeg_data[name]
            stats[name] = {
                "min": float(channel_data.min()),
                "max": float(channel_data.max()),
                "mean": float(channel_data.mean()),
                "std": float(channel_data.std())
            }
        
        print("Sending plot and stats to frontend")
        socketio.emit('experiment_update', {
            "message": "EEG data plotted and analyzed",
            "action": "display_plot",
            "plot": plot_data_base64,
            "plotTitle": "EEG Waveforms from Alternate CSV",
            "stats": json.dumps(stats)
        })

    except Exception as e:
        print(f"Error in experiment: {str(e)}")
        socketio.emit('experiment_error', {"message": str(e)})
    finally:
        print("Alternate CSV data plotting experiment completed")
        socketio.emit('experiment_update', {"message": "Alternate CSV data plotting experiment completed"})
