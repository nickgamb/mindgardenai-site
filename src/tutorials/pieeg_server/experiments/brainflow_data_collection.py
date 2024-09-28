import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path=None, wait_for_file=None):
    socketio.emit('experiment_update', {
        "message": "Starting BrainFlow data collection experiment",
        "action": "open_terminal",
        "terminalTitle": "BrainFlow Data Collection"
    })

    params = BrainFlowInputParams()
    params.serial_port = '/dev/spidev0.0'  # Adjust if needed
    board = BoardShim(BoardIds.PIEEG_BOARD.value, params)

    try:
        board.prepare_session()
        board.start_stream()
        socketio.emit('experiment_update', {
            "message": "[INFO] Stream started, collecting data for 10 seconds...",
            "action": "append_terminal"
        })
        time.sleep(10)
        data = board.get_board_data()
        board.stop_stream()
        board.release_session()

        # Save data to CSV
        filename = 'pieeg_data.csv'
        np.savetxt(filename, data.T, delimiter=',')
        socketio.emit('experiment_update', {
            "message": f"[SUCCESS] Data saved to {filename}",
            "action": "append_terminal"
        })

    except Exception as e:
        socketio.emit('experiment_error', {"message": str(e)})
    finally:
        socketio.emit('experiment_update', {
            "message": "BrainFlow data collection experiment completed",
            "action": "close_terminal"
        })

# Indicate that this experiment doesn't require a file upload
run.requires_file = False