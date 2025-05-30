# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Foundational symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: admin@mindgardenai.com
#v0.1a
import logging
import json
from flask import Flask, render_template, request, jsonify, Response
import spidev
import gpiod
import threading
import time
from scipy.signal import butter, filtfilt, iirnotch
import numpy as np
from flask_socketio import SocketIO, emit
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import os
import asyncio
import inspect
import sqlite3
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app)

# Global variables for SPI and GPIO
spi = None
chip = None
line = None

# BrainFlow specific settings
params = BrainFlowInputParams()
params.serial_port = '/dev/spidev0.0'

# Global variables for Experiments
experiments = {}
current_experiment = None
experiment_file_path = None
experiment_event = threading.Event()
experiment_thread = None

def initialize_spi_gpio():
    global spi, chip, line
    try:
        logging.info("Initializing SPI...")
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 600000
        spi.lsbfirst = False
        spi.mode = 0b01
        spi.bits_per_word = 8
        logging.info("SPI setup complete.")
    except Exception as e:
        logging.error(f"SPI setup error: {e}")
        raise

    try:
        logging.info("Initializing GPIO...")
        chip = gpiod.Chip('/dev/gpiochip0')
        line = chip.get_line(26)
        line.request(consumer="app", type=gpiod.LINE_REQ_EV_FALLING_EDGE)
        logging.info("GPIO setup complete.")
    except Exception as e:
        logging.error(f"GPIO setup error: {e}")
        raise

def cleanup_spi_gpio():
    global spi, chip, line
    try:
        logging.info("Cleaning up SPI and GPIO...")
        if spi:
            spi.close()
            spi = None
            logging.info("SPI closed.")
        if line:
            line.release()
            line = None
            logging.info("GPIO line released.")
        if chip:
            chip.close()
            chip = None
            logging.info("GPIO chip closed.")
    except Exception as e:
        logging.error(f"SPI and GPIO cleanup error: {e}")

def check_gpio_conflicts():
    try:
        # Attempt to open the GPIO line to see if it's already in use
        test_chip = gpiod.Chip('/dev/gpiochip0')
        test_line = test_chip.get_line(26)
        test_line.request(consumer="test", type=gpiod.LINE_REQ_EV_FALLING_EDGE)
        test_line.release()
        test_chip.close()
        return False  # No conflicts
    except Exception:
        return True  # Conflicts detected

# Registers for ADS1299
reset = 0x06
start = 0x08
stop = 0x0A
rdatac = 0x10
sdatac = 0x11
wakeup = 0x02

def read_byte(register):
    if not spi:
        logging.error("SPI not initialized.")
        return None
    write = 0x20
    register_write = write | register
    data = [register_write, 0x00, register]
    read_reg = spi.xfer(data)
    logging.info(f"Read byte: {read_reg}")
    return read_reg

def send_command(command):
    if not spi:
        logging.error("SPI not initialized.")
        return None
    send_data = [command]
    com_reg = spi.xfer(send_data)
    logging.info(f"Sent command: {command}")

def write_byte(register, data):
    if not spi:
        logging.error("SPI not initialized.")
        return None
    write = 0x40
    register_write = write | register
    data = [register_write, 0x00, data]
    logging.info(f"Write byte: {data}")
    spi.xfer(data)

def configure_ads1299(gain, enabled_channels, ref_enabled, biasout_enabled):
    try:
        send_command(wakeup)
        send_command(stop)
        send_command(reset)
        send_command(sdatac)

        write_byte(0x14, 0x80)  # GPIO
        write_byte(0x01, 0x96)  # Config1
        write_byte(0x02, 0xD4)  # Config2
        write_byte(0x03, 0xE0)  # Config3

        for ch in range(8):
            channel_config = gain if ch < enabled_channels else 0x80
            logging.info(f"Configuring channel {ch + 1} with gain: {channel_config}")
            write_byte(0x05 + ch, channel_config)

        write_byte(0x05 + 8, 0x10 if ref_enabled else 0x80)
        write_byte(0x05 + 9, 0x10 if biasout_enabled else 0x80)

        send_command(rdatac)
        send_command(start)
        logging.info("ADS1299 configuration complete.")
    except Exception as e:
        logging.error(f"ADS1299 configuration error: {e}")
        raise

# Initialize the variables
enabled_channels = 8  # Default to 8 channels enabled
ref_enabled = True  # Default to REF enableds
biasout_enabled = True  # Default to BIASOUT enabled
lowcut = 0.1
highcut = 30
order = 5
fs = 250  # Sampling frequency
bandpass_enabled = False
smoothing_enabled = False
baseline_correction_enabled = False
acquisition_method = "brainflow"  # Default acquisition method

# Set up 8 ch for read data
collected_data = []

calibration_values = [0] * 8

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    if len(data) <= order * 6:  # Increased multiplier for safety
        logging.warning(f"Not enough data points to apply filter: {len(data)} points available, {order * 6} needed.")
        return data  # Return unfiltered data if not enough points
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)  # Using filtfilt for zero-phase filtering
    return y

def notch_filter(data, fs, freq=50, Q=30):
    b, a = iirnotch(freq, Q, fs)
    y = filtfilt(b, a, data)
    return y

def moving_average(data, window_size=5):
    if len(data) < window_size:
        return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def remove_artifacts(data, threshold=5):
    mean_value = np.mean(data)
    data = np.where(np.abs(data) > threshold, mean_value, data)
    return data

def read_eeg_data():
    global collected_data
    collected_data = [[] for _ in range(enabled_channels)]
    while running:
        try:
            event = line.event_read()
            output = spi.readbytes(27)
            channel_data = []
            for i in range(3, 25, 3):
                voltage = (output[i] << 16) | (output[i + 1] << 8) | output[i + 2]
                if voltage & 0x800000:
                    voltage -= 1 << 24
                voltage = voltage * (4.5 / (2 ** 23 - 1))  # Convert to voltage
                channel_data.append(voltage)

            logging.info(f"Raw SPI output: {output}")
            for idx, val in enumerate(channel_data):
                logging.info(f"Manually extracted Channel {idx + 1} data: {val}")

            for idx in range(enabled_channels):
                collected_data[idx].append(channel_data[idx])

            if baseline_correction_enabled:
                for idx in range(enabled_channels):
                    collected_data[idx][-1] -= calibration_values[idx]

            filtered_data = channel_data.copy()
            if bandpass_enabled:
                filtered_data = [butter_bandpass_filter(collected_data[idx], lowcut, highcut, fs, order)[-1] for idx in range(enabled_channels)]

            smoothed_data = filtered_data.copy()
            if smoothing_enabled:
                smoothed_data = [moving_average(filtered_data[idx])[-1] if len(filtered_data[idx]) >= 5 else filtered_data[idx] for idx in range(enabled_channels)]

            logging.info(f"Unfiltered data: {channel_data}")
            logging.info(f"Filtered data: {filtered_data}")
            logging.info(f"Smoothed data: {smoothed_data}")

            socketio.emit('update_data', {
                'raw': channel_data,
                'filtered': filtered_data,
                'smoothed': smoothed_data
            })

        except Exception as e:
            logging.error(f"Error reading data: {e}")
            time.sleep(1)
            continue

def read_eeg_data_brainflow():
    global collected_data
    try:
        board = BoardShim(BoardIds.PIEEG_BOARD.value, params)
        board.prepare_session()
        board.start_stream(45000, '')

        while running:
            data = board.get_current_board_data(250)
            eeg_channels = BoardShim.get_eeg_channels(BoardIds.PIEEG_BOARD.value)
            data_transposed = data[eeg_channels, :]

            logging.info(f"Raw BrainFlow data: {data_transposed}")

            if data_transposed.size == 0:
                logging.error("No data retrieved from BrainFlow")
                continue

            # Apply BrainFlow filters if enabled
            if bandpass_enabled:  # Assume this variable is set based on the checkbox
                for channel in eeg_channels:
                    try:
                        DataFilter.detrend(data_transposed[channel], DetrendOperations.CONSTANT.value)
                        DataFilter.perform_bandpass(data_transposed[channel], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 3.0, 45.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                        DataFilter.perform_bandstop(data_transposed[channel], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 48.0, 52.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                        DataFilter.perform_bandstop(data_transposed[channel], BoardShim.get_sampling_rate(BoardIds.PIEEG_BOARD.value), 58.0, 62.0, 2, FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
                    except Exception as e:
                        logging.error(f"Error applying filters to channel {channel}: {e}")

            # Apply baseline correction if enabled
            if baseline_correction_enabled:  # Assume this variable is set based on the checkbox
                for idx in range(len(eeg_channels)):
                    data_transposed[idx] -= calibration_values[idx]

            # Normalize REF channel if necessary
            ref_channel_index = 0  # Assuming REF channel is the first in eeg_channels
            ref_values = data_transposed[ref_channel_index]
            ref_mean = ref_values.mean()
            ref_std = ref_values.std()

            logging.info(f"REF Channel - Mean: {ref_mean}, Std Dev: {ref_std}")

            # Normalize if the mean is significantly higher than expected
            if ref_mean > 1000:  # This threshold can be adjusted based on expected range
                data_transposed[ref_channel_index] = (ref_values - ref_mean) / ref_std
                logging.info(f"Normalized REF Channel - Mean: {data_transposed[ref_channel_index].mean()}, Std Dev: {data_transposed[ref_channel_index].std()}")

            data_transposed = data_transposed.tolist()  # Convert to list for easier processing
            
            # Reset collected_data for each new read
            collected_data = [[] for _ in range(len(eeg_channels))]
            
            for idx, channel_data in enumerate(data_transposed):
                collected_data[idx].extend(channel_data)
                
            logging.info(f"Processed BrainFlow data: {data_transposed}")
            
            socketio.emit('update_data', {
                'raw': [channel[0] for channel in data_transposed]  # Send only the latest data points
            })
            time.sleep(1)

        board.stop_stream()
        board.release_session()
    except BrainFlowError as e:
        logging.error(f"BrainFlow error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def calibrate_brainflow():
    global calibration_values
    try:
        logging.info("Starting BrainFlow calibration process")
        board = BoardShim(BoardIds.PIEEG_BOARD.value, params)
        board.prepare_session()
        board.start_stream(45000, '')

        calibration_duration = 5  # seconds
        calibration_data = [[] for _ in range(enabled_channels)]

        start_time = time.time()
        while time.time() - start_time < calibration_duration:
            data = board.get_current_board_data(250)
            eeg_channels = BoardShim.get_eeg_channels(BoardIds.PIEEG_BOARD.value)
            data_transposed = data[eeg_channels, :]

            if data_transposed.size == 0:
                logging.error("No data retrieved from BrainFlow")
                continue

            for idx, channel_data in enumerate(data_transposed):
                calibration_data[idx].extend(channel_data)

        calibration_values = [np.mean(ch_data) for ch_data in calibration_data]
        logging.info(f"BrainFlow calibration values: {calibration_values}")

        board.stop_stream()
        board.release_session()

    except BrainFlowError as e:
        logging.error(f"BrainFlow calibration error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected calibration error: {e}")

# Functions supporting experiments feature

def load_experiments():
    global experiments
    experiments_dir = os.path.join(os.path.dirname(__file__), 'experiments')
    for filename in os.listdir(experiments_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = __import__(f'experiments.{module_name}', fromlist=['run'])
            experiments[module_name] = module.run
    print(f"Loaded experiments: {list(experiments.keys())}")

def run_experiment(experiment_name):
    global current_experiment, experiment_thread, running

    if experiment_name in experiments:
        if experiment_thread and experiment_thread.is_alive():
            return jsonify({"status": "error", "message": "An experiment is already running"})
        
        running = True
        experiment_thread = threading.Thread(target=execute_experiment, args=(experiment_name,))
        experiment_thread.start()
        return jsonify({"status": "success", "message": f"Experiment {experiment_name} started"})
    else:
        return jsonify({"status": "error", "message": "Experiment not found"})

def execute_experiment(experiment_name):
    global current_experiment, running, experiment_file_path, experiment_event
    if experiment_name in experiments:
        print(f"Starting experiment: {experiment_name}")
        current_experiment = experiments[experiment_name]
        experiment_file_path = None
        experiment_event.clear()
        cleanup_spi_gpio()  #clean up spi_gpio before running. 
        try:
            # Check if the experiment requires a file upload
            requires_file = getattr(current_experiment, 'requires_file', True)
            
            # Prepare arguments
            args = {
                'read_eeg_data': read_eeg_data,
                'read_eeg_data_brainflow': read_eeg_data_brainflow,
                'acquisition_method': acquisition_method,
                'socketio': socketio,
                'running': lambda: running,
                'get_file_path': lambda: experiment_file_path if requires_file else None,
                'wait_for_file': experiment_event.wait if requires_file else lambda _: True
            }
            
            # Check if the experiment is asynchronous
            if inspect.iscoroutinefunction(current_experiment):
                # Run asynchronous experiment
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(current_experiment(**args))
            else:
                # Run synchronous experiment
                current_experiment(**args)
                
        except Exception as e:
            logging.error(f"Error in experiment {experiment_name}: {e}")
            socketio.emit('experiment_error', {"message": str(e)})
        finally:
            running = False
            experiment_thread = None
            current_experiment = None
    else:
        logging.error(f"Experiment {experiment_name} not found")
        socketio.emit('experiment_error', {"message": f"Experiment {experiment_name} not found"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-analysis', methods=['POST'])
def start_analysis():
    global running
    running = True
    if acquisition_method == "spi":
        initialize_spi_gpio()
        threading.Thread(target=read_eeg_data, daemon=True).start()
    else:
        cleanup_spi_gpio()  # Ensure no conflicts before starting BrainFlow
        if check_gpio_conflicts():
            return jsonify({"status": "GPIO conflict detected. Please resolve before starting BrainFlow."}), 409
        threading.Thread(target=read_eeg_data_brainflow, daemon=True).start()
    return jsonify({"status": "Analysis started"})

@app.route('/stop-analysis', methods=['POST'])
def stop_analysis():
    global running
    running = False
    time.sleep(1)  # Ensure threads have time to exit
    cleanup_spi_gpio()
    socketio.emit('analysis_stopped')  # Notify frontend to update the settings
    return jsonify({"status": "Analysis stopped"})

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global calibration_values, spi, line
    calibration_duration = 5  # seconds
    calibration_data = [[] for _ in range(enabled_channels)]

    # Check the acquisition method and proceed accordingly
    if acquisition_method == "spi":
        # Ensure SPI and GPIO are initialized
        if spi is None or line is None:
            logging.info("Re-initializing SPI and GPIO for calibration")
            initialize_spi_gpio()

        start_time = time.time()
        logging.info("Starting calibration process")
        while time.time() - start_time < calibration_duration:
            try:
                logging.info("Waiting for GPIO event")
                event = line.event_read()
                logging.info("GPIO event read")

                logging.info("Reading SPI data")
                output = spi.readbytes(27)
                logging.info(f"SPI data read: {output}")

                for a in range(3, 25, 3):
                    voltage_1 = (output[a] << 16) | (output[a + 1] << 8) | output[a + 2]
                    if voltage_1 & 0x800000:
                        voltage_1 -= 1 << 24
                    voltage_1 = voltage_1 * (4.5 / (2 ** 23 - 1))  # Convert to voltage
                    channel_num = (a // 3) - 1  # Adjusted calculation for channel_num
                    if 0 <= channel_num < len(calibration_data):
                        calibration_data[channel_num].append(voltage_1)
                logging.info(f"Read data: {output}")
            except Exception as e:
                logging.error(f"Error during calibration: {e}")
                break

        logging.info(f"Calibration data: {calibration_data}")
        calibration_values = [np.mean(ch_data) for ch_data in calibration_data]
        logging.info(f"Calibration values: {calibration_values}")
        cleanup_spi_gpio()
    else:
        calibrate_brainflow()

    return jsonify({"status": "Calibration completed", "values": calibration_values})

@app.route('/update-settings', methods=['POST'])
def update_settings():
    global lowcut, highcut, order, baseline_correction_enabled, enabled_channels, ref_enabled, biasout_enabled, bandpass_enabled, smoothing_enabled, acquisition_method
    data = request.json
    lowcut = float(data.get('lowcut', lowcut))
    highcut = float(data.get('highcut', highcut))
    order = int(data.get('order', order))
    baseline_correction_enabled = data.get('baseline_correction_enabled', baseline_correction_enabled)
    enabled_channels = int(data.get('enabled_channels', enabled_channels))
    ref_enabled = data.get('ref_enabled', ref_enabled)
    biasout_enabled = data.get('biasout_enabled', biasout_enabled)
    bandpass_enabled = data.get('bandpass_filter_enabled', bandpass_enabled)
    smoothing_enabled = data.get('smoothing_enabled', smoothing_enabled)
    acquisition_method = data.get('acquisition_method', acquisition_method)
    logging.info(f"Updated settings: lowcut={lowcut}, highcut={highcut}, order={order}, baseline_correction_enabled={baseline_correction_enabled}, enabled_channels={enabled_channels}, ref_enabled={ref_enabled}, biasout_enabled={biasout_enabled}, bandpass_enabled={bandpass_enabled}, smoothing_enabled={smoothing_enabled}, acquisition_method={acquisition_method}")
    if acquisition_method == "spi":
        initialize_spi_gpio()
        configure_ads1299(int(data.get('gain', 0)), enabled_channels, ref_enabled, biasout_enabled)
    return jsonify({"status": "Settings updated"})

# Function to create CSV data
def create_csv(data):
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Channel' + str(i+1) for i in range(len(data))])
    for row in zip(*data):
        writer.writerow(row)
    output.seek(0)
    return output.getvalue()

@app.route('/export-data')
def export_data():
    try:
        num_rows = int(request.args.get('num_rows', 5000))
        if num_rows > len(collected_data[0]):
            num_rows = len(collected_data[0])
        csv_data = create_csv([ch[:num_rows] for ch in collected_data])
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=eeg_data.csv'}
        )
    except Exception as e:
        logging.error(f"Error exporting data: {e}")
        return Response(
            "Internal Server Error",
            status=500
        )

# Routes for the Experiments feature

@app.route('/get_experiments')
def get_experiments():
    return jsonify(list(experiments.keys()))

@app.route('/run_experiment', methods=['POST'])
def start_experiment():
    experiment_name = request.json.get('experiment')
    return run_experiment(experiment_name)

@app.route('/stop_experiment', methods=['POST'])
def stop_experiment():
    global current_experiment, experiment_thread, running
    running = False
    experiment_event.set()  # Signal the experiment to stop if it's waiting for a file
    if experiment_thread is not None and experiment_thread.is_alive():
        experiment_thread.join(timeout=5)
        if experiment_thread.is_alive():
            return jsonify({"status": "error", "message": "Failed to stop experiment"}), 500
    experiment_thread = None
    current_experiment = None
    return jsonify({"status": "success", "message": "Experiment stopped"})

@app.route('/get_features/<session_id>', methods=['GET'])
def get_features(session_id):
    logging.info(f"Fetching features for session '{session_id}'")
    conn = sqlite3.connect('brainwave_enrollments.db')
    c = conn.cursor()
    logging.info("Enrollments database connected.")
    
    # Add this line to check all available sessions
    c.execute('SELECT DISTINCT session_id FROM enrollments')
    available_sessions = c.fetchall()
    logging.info(f"Available sessions in the database: {available_sessions}")
    
    c.execute('SELECT label, features FROM enrollments WHERE session_id = ?', (session_id,))
    features = c.fetchall()
    conn.close()
    
    # Convert bytes to base64 encoded string
    processed_features = [(label, base64.b64encode(feature_bytes).decode('utf-8')) 
                          for label, feature_bytes in features]
    
    logging.info(f"Fetched and processed features: {processed_features}")
    return jsonify(processed_features)

@socketio.on('set_file_path')
def set_file_path(file_content):
    global experiment_file_path, experiment_event
    print("Received file content, length:", len(file_content))
    # Save the file content to a temporary file
    temp_file_path = 'temp_data.csv'
    with open(temp_file_path, 'w') as f:
        f.write(file_content)
    
    print(f"Saved file content to {temp_file_path}")
    
    experiment_file_path = temp_file_path
    experiment_event.set()  # Signal that the file is ready

if __name__ == '__main__':
    running = False
    collected_data = [[] for _ in range(enabled_channels)]
    load_experiments()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

