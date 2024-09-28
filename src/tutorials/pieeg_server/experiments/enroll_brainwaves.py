import time
import random
import sqlite3
import logging
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import json
from scipy import signal
from scipy.stats import skew, kurtosis
from scipy.signal import welch
from datetime import datetime
from brainflow import DataFilter, DetrendOperations, FilterTypes, BoardShim, BrainFlowInputParams, BoardIds

# Global variable to store EEG data for each task
task_data_list = []

def plot_eeg_task_data(data, task_name):
    data = data.astype(float)
    eeg_data = data
    timestamps = np.arange(eeg_data.shape[1]) / 250  # Assuming a sampling rate of 250 Hz

    plt.figure(figsize=(3, 3))  # Smaller square plot

    channel_names = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "O1", "O2"]

    for i, name in enumerate(channel_names):
        plt.plot(timestamps, eeg_data[i, :], label=name, linewidth=0.5, alpha=0.8)

    plt.title(f'{task_name} EEG Waveforms', fontsize=8)
    plt.xlabel('Time (seconds)', fontsize=8)
    plt.ylabel('Voltage', fontsize=8)
    plt.legend(loc='upper right', fontsize='xx-small')
    plt.grid(True, alpha=0.5)

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')  # Reduce dpi for smaller file size
    buf.seek(0)
    plt.close()
    return buf.getvalue()

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path, wait_for_file):
    logging.info("Starting Enroll Brainwaves experiment")
    
    socketio.emit('experiment_update', {
        "message": "Starting Enroll Brainwaves experiment",
        "action": "open_popup"
    })

    time.sleep(0.5)  # Adding delay to ensure event is processed

    user_id = "user1"  # In a real application, you'd get this from user input or session
    conn = setup_database()
    session_id = get_next_session_id(conn, user_id)

    # Step 1: Introduction
    socketio.emit('experiment_update', {
        "message": "Please follow the prompts to enroll your brainwaves.",
        "action": "show_instruction"
    })

    time.sleep(5)

    socketio.emit('experiment_update', {
        "message": "",
        "action": "hide_instruction"
    })

    time.sleep(3)  # Adding delay to ensure event is processed

    # Step 2: Perform tasks and record EEG data samples
    tasks = [
        ("baseline", "In a quiet environment, free of distractions, focus on the image before you. Try not to move or blink and concentrate only on the image.", "checkered_grid", None),
        ("meditation", "Continuing to free your mind of distractions, breathe in as the circle expands and out as the circle shrinks.", "breathing_circle", {"expand_time": 4, "hold_time": 4, "shrink_time": 4}),
        ("word_focus", "Focus on the following words as they appear", "text", ["TREE", "BOOK", "RIVER", "CLOUD", "CHAIR"]),
        ("actions", "Please perform the following actions", "text", [
            ("blink your eyes", "blink"),
            ("move your right hand fingers", "fingers_right"),
            ("move your left hand fingers", "fingers_left"),
            ("smile", "face_happy"),
            ("frown", "face_sad"),
            ("keep a neutral face", "face_neutral")
        ])
    ]

    for task_name, instruction, visual_type, visual_data in tasks:
        if not running():  # Check if we should continue running
            break

        if task_name == "baseline":
            logging.info(f"Starting {task_name} tasks.")
            run_step(socketio, instruction, 30, task_name, visual_type, visual_data, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)

        elif task_name == "meditation":
            logging.info(f"Starting {task_name} tasks.")
            run_step(socketio, instruction, 30, task_name, visual_type, visual_data, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)

        elif task_name == "word_focus":
            logging.info(f"Starting {task_name} tasks.")
            for word in random.sample(visual_data, 5):
                run_step(socketio, f"Focus on the word: {word}", 30, f"word_{word.lower()}", "text", {"text": word}, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)
        
        elif task_name == "actions":
            logging.info(f"Starting {task_name} tasks.")
            for action_text, action_label in visual_data:
                run_step(socketio, instruction, 30, action_label, "text", {"text": action_text}, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)

        else:
            run_step(socketio, instruction, 30, task_name, visual_type, visual_data, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)
            logging.info("Running unhandled tasks")

    conn.close()
    logging.info("Enrollment complete. Data saved to database.")

    time.sleep(1)

    # Step 3: Show Results
    socketio.emit('experiment_update', {
        "message": f"Brainwave enrollment complete for {user_id}. Session: {session_id}. Please run this enrollment multiple times to enhance training data.",
        "action": "show_instruction"
    })

    socketio.emit('experiment_update', {
        "message": "Showing embedded plots",
        "action": "show_embedded_plot",
        "sessionId": session_id 
    })

def setup_database():
    conn = sqlite3.connect('brainwave_enrollments.db')
    c = conn.cursor()
    
    # Enable foreign keys
    c.execute('PRAGMA foreign_keys = ON')
    
    # Create enrollments table
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT,
                  session_id INTEGER,
                  timestamp TEXT,
                  label TEXT,
                  features BLOB,
                  FOREIGN KEY(user_id) REFERENCES user_sessions(user_id))''')
    
    # Create user_sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                 (user_id TEXT PRIMARY KEY,
                  session_count INTEGER)''')
    
    # Create indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON enrollments(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON enrollments(session_id)')
    
    conn.commit()
    return conn

def get_next_session_id(conn, user_id):
    c = conn.cursor()
    c.execute('SELECT session_count FROM user_sessions WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result is None:
        c.execute('INSERT INTO user_sessions (user_id, session_count) VALUES (?, 1)', (user_id,))
        session_id = 1
    else:
        session_id = result[0] + 1
        c.execute('UPDATE user_sessions SET session_count = ? WHERE user_id = ?', (session_id, user_id))
    conn.commit()
    return session_id

def extract_features(eeg_data, fs=250):
    # Ensure data is 2D with channels as rows and time points as columns
    if eeg_data.ndim != 2:
        logging.error("eeg_data should be a 2D array with shape (channels, time points)")
        return None
    
    # Time-domain features
    mean = np.mean(eeg_data, axis=1)
    variance = np.var(eeg_data, axis=1)
    skewness = skew(eeg_data, axis=1)
    kurt = kurtosis(eeg_data, axis=1)
    
    # Frequency-domain features using Welch's method
    freqs, psd = signal.welch(eeg_data, fs=fs, nperseg=fs, axis=1)
    
    # Define frequency bands
    bands = [(1, 4), (4, 8), (8, 13), (13, 30), (30, 50)]  # Delta, Theta, Alpha, Beta, Gamma
    
    # Calculate power in different frequency bands
    band_power = []
    for low, high in bands:
        mask = (freqs >= low) & (freqs <= high)
        band_power.append(np.sum(psd[:, mask], axis=1))
    
    band_power = np.array(band_power).T  # Transpose to match shape (channels, bands)
    
    # Concatenate all features into a single 1D feature vector per channel
    features = np.concatenate([mean, variance, skewness, kurt] + [band_power.flatten()])
    
    return features

def extract_enhanced_features(eeg_data, fs=250):
    """
    Extract an enhanced set of features from EEG data.
    
    :param eeg_data: 2D numpy array of shape (channels, samples)
    :param fs: Sampling frequency
    :return: 1D numpy array of features
    """
    # Time-domain features
    mean = np.mean(eeg_data, axis=1)
    variance = np.var(eeg_data, axis=1)
    skewness = scipy.stats.skew(eeg_data, axis=1)
    kurt = scipy.stats.kurtosis(eeg_data, axis=1)
    
    # Frequency-domain features
    freqs, psd = signal.welch(eeg_data, fs=fs, nperseg=fs*2)
    
    # Define frequency bands
    bands = [(0.5, 4), (4, 8), (8, 13), (13, 30), (30, 100)]  # Delta, Theta, Alpha, Beta, Gamma
    
    # Calculate relative band powers
    total_power = np.sum(psd, axis=1)
    band_powers = []
    for low, high in bands:
        mask = (freqs >= low) & (freqs <= high)
        band_power = np.sum(psd[:, mask], axis=1) / total_power
        band_powers.append(band_power)
    
    # Connectivity features (simple correlation between channels)
    connectivity = np.corrcoef(eeg_data).flatten()
    
    # Combine all features
    features = np.concatenate([mean, variance, skewness, kurt] + band_powers + [connectivity])
    
    return features

def check_eeg_data_quality(eeg_data, min_voltage=-500, max_voltage=500, min_variance=0.01):
    """
    Check if the EEG data is of sufficient quality for processing.
    
    :param eeg_data: 2D numpy array of shape (channels, samples)
    :param min_voltage: Minimum acceptable voltage (μV)
    :param max_voltage: Maximum acceptable voltage (μV)
    :param min_variance: Minimum variance required in the signal
    :return: Boolean indicating if the data is of sufficient quality
    """
    # Check if data is within acceptable voltage range
    if np.any(eeg_data < min_voltage) or np.any(eeg_data > max_voltage):
        min_val = np.min(eeg_data)
        max_val = np.max(eeg_data)
        #logging.warning(f"EEG data contains values outside the acceptable range. Min: {min_val:.2f}, Max: {max_val:.2f}")
        return False
    
    # Check if data has sufficient variance (not flat or near-flat)
    variances = np.var(eeg_data, axis=1)
    if np.any(variances < min_variance):
        min_var = np.min(variances)
        #logging.warning(f"EEG data has insufficient variance. Minimum variance: {min_var:.6f}")
        return False
    
    #logging.info("EEG data quality check passed")
    return True

def record_eeg_data(socketio, duration, label, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running):
    global task_data_list
    c = conn.cursor()

    params = BrainFlowInputParams()
    params.serial_port = '/dev/spidev0.0'
    board = BoardShim(BoardIds.PIEEG_BOARD.value, params)

    try:
        logging.info("Starting BrainFlow session")
        running = True
        board.prepare_session()
        board.start_stream(45000, '')

        collected_data = []
        nan_count = 0
        total_samples = 0

        start_time = time.time()
        logging.info(f"Streaming for {duration} seconds")
        while time.time() - start_time < duration:
            data = board.get_current_board_data(250)
            eeg_channels = BoardShim.get_eeg_channels(BoardIds.PIEEG_BOARD.value)
            data_transposed = data[eeg_channels, :]

            if data_transposed.size == 0:
                continue
            else:
                total_samples += 1
                filtered_data = np.zeros_like(data_transposed)

                for i, channel in enumerate(eeg_channels):
                    try:
                        channel_data = data_transposed[i].copy()
                        DataFilter.detrend(channel_data, DetrendOperations.CONSTANT.value)
                        DataFilter.perform_bandpass(channel_data, BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 0.5, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                        DataFilter.perform_bandstop(channel_data, BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                        DataFilter.perform_bandstop(channel_data, BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 58.0, 62.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                        filtered_data[i] = channel_data
                    except Exception as e:
                        logging.error(f"Error applying filters to channel {i}: {e}")

                # Check for NaN values
                if np.isnan(filtered_data).any():
                    logging.warning("NaN values detected in filtered data. Skipping this sample.")
                    nan_count += 1
                else:
                    collected_data.append(filtered_data)

        logging.info("Stopping stream.")
        board.stop_stream()
        board.release_session()

        logging.info(f"Total samples processed: {total_samples}")
        logging.info(f"Samples with NaN values (skipped): {nan_count}")
        logging.info(f"Clean samples collected: {len(collected_data)}")

        if collected_data:
            all_data = np.hstack(collected_data)

            if check_eeg_data_quality(all_data):
                logging.info("EEG data quality check passed")
            else:
                logging.info("Low quality data detected, but proceeding with feature extraction.")

            logging.info("Extracting features from EEG Data")
            try:
                features = extract_enhanced_features(all_data)
                if features is None:
                    raise ValueError("Feature extraction returned None")

                logging.info("Writing EEG Data to Database")
                timestamp = datetime.now().isoformat()

                c.execute('''INSERT INTO enrollments 
                                (user_id, session_id, timestamp, label, features)
                                VALUES (?, ?, ?, ?, ?)''',
                            (user_id, session_id, timestamp, label, features.tobytes()))
                conn.commit()
                logging.info(f"Data for label '{label}' successfully stored in database")

            except Exception as e:
                logging.error(f"Error during feature extraction or database operations: {e}")

        else:
            logging.warning("No clean data collected. Skipping database insertion.")

        time.sleep(1)
        running = False
        socketio.emit('analysis_stopped')  # Notify frontend to update the settings

    except Exception as e:
        socketio.emit('experiment_error', {"message": str(e)})
        logging.error(f"Error in record_eeg_data: {e}")
    finally:
        if board.is_prepared():
            board.stop_stream()
            board.release_session()
        logging.info(f"EEG data recording for label '{label}' completed.")

def run_step(socketio, instruction, duration, label, visual_type, visual_data, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running):
    socketio.emit('experiment_update', {
        "message": instruction,
        "action": "show_instruction"
    })

    time.sleep(1)
    
    if visual_type:
        socketio.emit('experiment_update', {
            "message": "",
            "action": f"show_{visual_type}",
            "data": visual_data
        })
    
    socketio.emit('experiment_update', {
        "message": "",
        "action": "show_progress_bar",
        "data": {"duration": duration}
    })
    
    record_duraction = duration - 10 #Offset duration used by progress bar to ensure operations end in time
    record_eeg_data(socketio, record_duraction, label, conn, user_id, session_id, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)

    socketio.emit('experiment_update', {
        "message": "",
        "action": "hide_progress_bar"
    })

    socketio.emit('experiment_update', {
        "message": "",
        "action": "hide_instruction"
    })

    if visual_type:
        socketio.emit('experiment_update', {
            "message": "",
            "action": f"hide_{visual_type}"
        })

    time.sleep(4)

# Indicate that this experiment doesn't require a file upload
run.requires_file = False
