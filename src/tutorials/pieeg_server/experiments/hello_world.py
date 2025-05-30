# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
# experiments/hello_world.py

import time
import logging

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path=None, wait_for_file=None):
    logging.info("Starting Hello World experiment")
    socketio.emit('experiment_update', {
        "message": "Hello World experiment started",
        "action": "open_terminal",
        "terminalTitle": "Hello World Experiment"
    })

    try:
        count = 0
        while running() and count < 10:
            if acquisition_method == "spi":
                data = read_eeg_data()
            else:
                data = read_eeg_data_brainflow()

            # Process the data (this is a simple example)
            avg_voltage = sum(data) / len(data) if data else 0
            
            message = f"[{time.strftime('%H:%M:%S')}] Hello World! Iteration {count + 1}. Average voltage: {avg_voltage:.2f}"
            socketio.emit('experiment_update', {
                "message": message,
                "action": "append_terminal"
            })

            time.sleep(1)  # Update every second
            count += 1

    except Exception as e:
        logging.error(f"Error in Hello World experiment: {e}")
        socketio.emit('experiment_error', {"message": str(e)})

    finally:
        socketio.emit('experiment_update', {
            "message": "Hello World experiment completed",
            "action": "close_terminal"
        })
        logging.info("Hello World experiment completed")

# Indicate that this experiment doesn't require a file upload
run.requires_file = False
