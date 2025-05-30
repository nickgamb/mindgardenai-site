# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: licensing@mindgarden.ai
import time
import logging
import numpy as np
import joblib
from scipy import signal, stats
from brainflow import DataFilter, DetrendOperations, FilterTypes, BoardShim, BrainFlowInputParams, BoardIds

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path=None, wait_for_file=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def emit_update(message, action=None, data=None):
        update = {"message": message}
        if action:
            update["action"] = action
        if data:
            update["data"] = data
        socketio.emit('experiment_update', update)

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

    def authenticate(features, model, label_encoder):
        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]
        user = label_encoder.inverse_transform([prediction])[0]
        confidence = probabilities[prediction]
        return user, confidence

    logging.info("Starting Real-time Authentication experiment")
    emit_update("Starting Real-time Authentication experiment", "open_popup")

    try:
        model = joblib.load('authentication_model.joblib')
        label_encoder = joblib.load('label_encoder.joblib')
        scaler = joblib.load('feature_scaler.joblib')
        logging.info("Loaded model, encoder, and scaler")
        emit_update("Loaded model, encoder, and scaler", "update_progress")

        duration = 30  # seconds
        emit_update("Please remain still and focus on a fixed point for 30 seconds", "show_instruction")
        emit_update(" ", "show_progress_bar", {"duration": duration})

        eeg_data = record_eeg_data(duration - 5, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)

        if eeg_data is not None:
            if check_eeg_data_quality(eeg_data):
                features = extract_features(eeg_data)
                features_scaled = scaler.transform([features])  # Scale the features
                user, confidence = authenticate(features_scaled[0], model, label_encoder)
                emit_update(f"Predicted User: {user}, Confidence: {confidence:.2f}", "show_results")

                if user == "user1" and confidence > 0.6:  # Adjust this threshold based on your needs
                    emit_update("User authenticated", "show_results")
                else:
                    emit_update("User not authenticated", "show_results")
            else:
                emit_update("Low quality EEG data detected. Please adjust the headset and try again.", "show_error")
        else:
            emit_update("Failed to acquire EEG data", "show_error")

    except Exception as e:
        logging.error(f"Error in Real-time Authentication experiment: {str(e)}")
        emit_update(f"Error: {str(e)}", "show_error")

    finally:
        logging.info("Real-time Authentication experiment completed")
        emit_update("Real-time Authentication experiment completed", "close_popup")

def record_eeg_data(duration, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running):
    params = BrainFlowInputParams()
    params.serial_port = '/dev/spidev0.0'
    board = BoardShim(BoardIds.PIEEG_BOARD.value, params)
    eeg_data = []

    try:
        logging.info("Starting BrainFlow session")
        board.prepare_session()
        board.start_stream(45000, '')

        start_time = time.time()
        logging.info(f"Streaming for {duration} seconds")
        while time.time() - start_time < duration:
            if not running():
                break
            data = board.get_current_board_data(250)
            eeg_channels = BoardShim.get_eeg_channels(BoardIds.PIEEG_BOARD.value)
            data_transposed = data[eeg_channels, :]

            if data_transposed.size == 0:
                continue

            for i, channel in enumerate(eeg_channels):
                try:
                    DataFilter.detrend(data_transposed[i], DetrendOperations.CONSTANT.value)
                    DataFilter.perform_bandpass(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 0.5, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                    DataFilter.perform_bandstop(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                    DataFilter.perform_bandstop(data_transposed[i], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 58.0, 62.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                except Exception as e:
                    logging.error(f"Error applying filters to channel {i}: {e}")

            eeg_data.append(data_transposed)

        logging.info("Stopping stream.")
        board.stop_stream()
        board.release_session()

        if eeg_data:
            all_data = np.hstack(eeg_data)
            return all_data

        return None

    except Exception as e:
        logging.error(f"Error recording EEG data: {e}")
        return None
    finally:
        logging.info("EEG data recording completed.")

