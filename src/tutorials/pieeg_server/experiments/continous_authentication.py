# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
import time
import logging
import numpy as np
import scipy.stats
from scipy import signal
from scipy.stats import mode
import joblib
from brainflow import DataFilter, DetrendOperations, FilterTypes, BoardShim, BrainFlowInputParams, BoardIds

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path=None, wait_for_file=None):
    logging.info("Starting Continuous Authentication experiment")
    socketio.emit('experiment_update', {
        "message": "Starting Continuous Authentication experiment",
        "action": "open_popup"
    })

    try:
        # Load the trained model, label encoder, and scaler
        model = joblib.load('authentication_model.joblib')
        label_encoder = joblib.load('label_encoder.joblib')
        scaler = joblib.load('feature_scaler.joblib')
        logging.info("Loaded model, encoder, and scaler")
        
        authentication_window = []
        window_size = 5  # Number of authentication attempts to consider
        check_interval = 10  # Seconds between each authentication check
        duration = 10  # Duration of each EEG recording in seconds

        while running():
            eeg_data = record_eeg_data(duration, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)
            
            if eeg_data is not None:
                if check_eeg_data_quality(eeg_data):
                    features = extract_features(eeg_data)
                    features_scaled = scaler.transform([features])
                    user, confidence = authenticate(features_scaled[0], model, label_encoder)
                    
                    authentication_window.append((user, confidence))
                    if len(authentication_window) > window_size:
                        authentication_window.pop(0)
                    
                    users, confidences = zip(*authentication_window)
                    most_common_user = mode(users).mode[0]
                    avg_confidence = np.mean(confidences)
                    
                    status = "Authenticated" if most_common_user == "user1" and avg_confidence > 0.6 else "Not Authenticated"
                    
                    socketio.emit('experiment_update', {
                        "message": f"Current Status: {status} (User: {most_common_user}, Confidence: {avg_confidence:.2f})",
                        "action": "update_results"
                    })
                else:
                    socketio.emit('experiment_update', {
                        "message": "Low quality EEG data detected. Please adjust the headset and try again.",
                        "action": "update_results"
                    })
                
                time.sleep(check_interval)

    except Exception as e:
        logging.error(f"Error in Continuous Authentication experiment: {str(e)}")
        socketio.emit('experiment_error', {"message": str(e)})

    finally:
        logging.info("Continuous Authentication experiment completed")
        socketio.emit('experiment_update', {
            "message": "Continuous Authentication experiment completed",
            "action": "close_popup"
        })

def check_eeg_data_quality(eeg_data, min_voltage=-500, max_voltage=500, min_variance=0.01):
    """
    Check if the EEG data is of sufficient quality for processing.
    
    :param eeg_data: 2D numpy array of shape (channels, samples)
    :param min_voltage: Minimum acceptable voltage (Î¼V)
    :param max_voltage: Maximum acceptable voltage (Î¼V)
    :param min_variance: Minimum variance required in the signal
    :return: Boolean indicating if the data is of sufficient quality
    """
    # Check if data is within acceptable voltage range
    if np.any(eeg_data < min_voltage) or np.any(eeg_data > max_voltage):
        min_val = np.min(eeg_data)
        max_val = np.max(eeg_data)
        logging.warning(f"EEG data contains values outside the acceptable range. Min: {min_val:.2f}, Max: {max_val:.2f}")
        return False
    
    variances = np.var(eeg_data, axis=1)
    if np.any(variances < min_variance):
        min_var = np.min(variances)
        logging.warning(f"EEG data has insufficient variance. Minimum variance: {min_var:.6f}")
        return False
    
    logging.info("EEG data quality check passed")
    return True

def extract_features(eeg_data, fs=250):
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

def authenticate(features, model, label_encoder):
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    user = label_encoder.inverse_transform([prediction])[0]
    confidence = probabilities[prediction]
    return user, confidence

def record_eeg_data(duration, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running):
    params = BrainFlowInputParams()
    params.serial_port = '/dev/spidev0.0'
    board = BoardShim(BoardIds.PIEEG_BOARD.value, params)
    eeg_data = []

    try:
        board.prepare_session()
        board.start_stream(45000, '')

        start_time = time.time()
        while time.time() - start_time < duration and running():
            data = board.get_current_board_data(250)
            eeg_channels = BoardShim.get_eeg_channels(BoardIds.PIEEG_BOARD.value)
            data_transposed = data[eeg_channels, :]

            if data_transposed.size == 0:
                continue

            for i, channel in enumerate(eeg_channels):
                DataFilter.detrend(data_transposed[i], DetrendOperations.CONSTANT.value)
                DataFilter.perform_bandpass(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 0.5, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                DataFilter.perform_bandstop(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                DataFilter.perform_bandstop(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 58.0, 62.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)

            eeg_data.append(data_transposed)

        board.stop_stream()
        board.release_session()

        if eeg_data:
            return np.hstack(eeg_data)
        return None

    except Exception as e:
        logging.error(f"Error recording EEG data: {e}")
        return None

# Indicate that this experiment doesn't require a file upload
run.requires_file = False
