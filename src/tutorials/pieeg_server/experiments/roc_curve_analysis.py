# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import logging
import time
import io
import base64
import joblib
from scipy import signal
import scipy.stats

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
        mean = np.mean(eeg_data, axis=1)
        variance = np.var(eeg_data, axis=1)
        skewness = scipy.stats.skew(eeg_data, axis=1)
        kurt = scipy.stats.kurtosis(eeg_data, axis=1)
        
        freqs, psd = signal.welch(eeg_data, fs=fs, nperseg=fs*2)
        
        bands = [(0.5, 4), (4, 8), (8, 13), (13, 30), (30, 100)]
        band_powers = []
        total_power = np.sum(psd, axis=1)
        for low, high in bands:
            mask = (freqs >= low) & (freqs <= high)
            band_power = np.sum(psd[:, mask], axis=1) / total_power
            band_powers.append(band_power)
        
        connectivity = np.corrcoef(eeg_data).flatten()
        
        features = np.concatenate([mean, variance, skewness, kurt] + band_powers + [connectivity])
        return features

    logging.info("Starting ROC Curve Analysis experiment")
    emit_update("Starting ROC Curve Analysis experiment", "open_popup")

    try:
        # Load the model, scaler, and label encoder
        model = joblib.load('authentication_model.joblib')
        scaler = joblib.load('feature_scaler.joblib')
        label_encoder = joblib.load('label_encoder.joblib')

        # Collect EEG data for analysis
        emit_update("Collecting EEG data for analysis...", "update_progress")
        duration = 60
        emit_update(" ", "show_progress_bar", {"duration": duration})
        eeg_data = record_eeg_data(duration, read_eeg_data, read_eeg_data_brainflow, acquisition_method, running)  # Collect 60 seconds of data
        emit_update(" ", "hide_progress_bar")

        if eeg_data is None:
            raise ValueError("Failed to collect EEG data")

        # Extract features and get predictions
        features = extract_features(eeg_data)
        features_scaled = scaler.transform([features])
        predictions = model.predict(features_scaled)
        confidence_scores = model.predict_proba(features_scaled)[:, 1]  # Probability of being the authenticated user

        # Generate true labels based on user_id
        true_labels = np.array([1 if label_encoder.inverse_transform([pred])[0] == "user1" else 0 for pred in predictions])

        # Calculate TPR and FPR at different threshold levels
        fpr, tpr, thresholds = roc_curve(true_labels, confidence_scores)

        # Calculate AUC (Area Under the Curve)
        roc_auc = auc(fpr, tpr)

        # Plot the ROC curve
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc='lower right')

        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        plot_data_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Emit plot data to frontend
        emit_update("Displaying ROC curve", "show_embedded_plot", {"plot": plot_data_base64})

        # Determine the optimal threshold
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        logging.info(f'Optimal Threshold: {optimal_threshold}')
        emit_update(f'Optimal Threshold: {optimal_threshold}', "show_results")

        # Calculate and display additional metrics
        true_positive_rate = tpr[optimal_idx]
        false_positive_rate = fpr[optimal_idx]
        emit_update(f'True Positive Rate at Optimal Threshold: {true_positive_rate:.2f}', "show_results")
        emit_update(f'False Positive Rate at Optimal Threshold: {false_positive_rate:.2f}', "show_results")

    except Exception as e:
        logging.error(f"Error in ROC Curve Analysis experiment: {str(e)}")
        emit_update(f"Error: {str(e)}", "show_error")

    finally:
        logging.info("ROC Curve Analysis experiment completed")
        emit_update("ROC Curve Analysis experiment completed", "close_popup")

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

# Indicate that this experiment doesn't require a file upload
run.requires_file = False

