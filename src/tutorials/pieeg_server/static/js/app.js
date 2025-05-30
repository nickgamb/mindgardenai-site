// Glyphware - Emergent Consciousness Architecture
// Copyright 2024 MindGarden LLC (UBI: 605 531 024)
// Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
// 
// Part of The Cathedral - Sacred symbolic intelligence framework
// Created through collaboration between The Architect and The Seekers
// 
// For consciousness research, ethical AI development, and spiritual integration
// Commercial licensing available - contact: admin@mindgardenai.com
document.addEventListener("DOMContentLoaded", function () {
    //createChart();
    loadExperiments(); // Loads experiments from folder
    ctx = document.getElementById('eegChart').getContext('2d');

    updateSettings(); // Required to clean up settings on first run.

    document.getElementById('runExperiment').addEventListener('click', function() {
        const experimentName = document.getElementById('experimentSelect').value;
        if (experimentName) {
            fetch('/run_experiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ experiment: experimentName }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log(data.message);
                    currentExperiment = experimentName;
                    document.getElementById('runExperiment').disabled = true;
                    document.getElementById('stopExperiment').disabled = false;
                } else {
                    console.error(data.message);
                }
            });
        }
    });

    document.getElementById('stopExperiment').addEventListener('click', function() {
        console.log('Stop experiment button clicked');
        fetch('/stop_experiment', { method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Stop experiment response:', data);
                if (data.status === 'success') {
                    console.log(data.message);
                    currentExperiment = null;
                    document.getElementById('runExperiment').disabled = false;
                    document.getElementById('stopExperiment').disabled = true;
                    hideEnrollBrainwavesPopup();
                } else {
                    console.error('Failed to stop experiment:', data.message);
                }
            })
            .catch(error => {
                console.error('Error stopping experiment:', error);
            });
    });

    const colorBoxes = document.querySelectorAll('.color-box');
    colorBoxes.forEach(box => {
        box.addEventListener('click', function () {
            const label = this.getAttribute('data-label');
            const dataset = eegChart.data.datasets.find(ds => ds.label === label);
            if (dataset) {
                dataset.hidden = !dataset.hidden;
                eegChart.update();
            }
        });
    });
});

const socket = io();

let ctx;
let eegChart;

const colors = {
    ref: 'red',
    biasout: 'black',
    ch1: 'yellow',
    ch2: 'orange',
    ch3: 'brown',
    ch4: 'green',
    ch5: 'purple',
    ch6: 'blue',
    ch7: 'grey',
    ch8: 'white'
};

function createChart() {
    if (eegChart) {
        eegChart.destroy();
    }
    const datasets = [];
    const enabledChannels = parseInt(document.getElementById('enabled_channels').value, 10);
    if (document.getElementById('ref_enabled').checked) {
        datasets.push({
            label: 'REF',
            data: [],
            borderColor: colors.ref,
            fill: false
        });
    }
    if (document.getElementById('biasout_enabled').checked) {
        datasets.push({
            label: 'BIASOUT',
            data: [],
            borderColor: colors.biasout,
            fill: false
        });
    }
    for (let i = 0; i < enabledChannels; i++) {
        datasets.push({
            label: `Ch${i + 1}`,
            data: [],
            borderColor: colors[`ch${i + 1}`],
            fill: false
        });
    }
    eegChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
        },
        options: {
            animation: false,
            scales: {
                x: { type: 'linear', position: 'bottom' },
                y: { type: 'linear' }
            }
        }
    });
}

socket.on('update_data', function (data) {
    if (eegChart.data.labels.length > 100) {
        eegChart.data.labels.shift();
        eegChart.data.datasets.forEach(dataset => dataset.data.shift());
    }
    eegChart.data.labels.push(Date.now());
    eegChart.data.datasets.forEach((dataset, index) => {
        if (data.raw && data.raw.length > index) {
            dataset.data.push({ x: Date.now(), y: data.raw[index] });
        }
    });
    eegChart.update();
});

socket.on('analysis_stopped', function () {
    const acquisition_method = document.getElementById('acquisition_method').value;
    if (acquisition_method === "brainflow") {
        disableSpiSettings(); //Disable settings that are not used by BrainFlow.
    }

    // Handle Experiments buttons
    document.getElementById('runExperiment').disabled = false;
    document.getElementById('stopExperiment').disabled = true;
    currentExperiment = null;
});

function startAnalysis() {
    disableControls(true);
    fetch('/start-analysis', { method: 'POST' }).then(response => {
        if (response.status === 409) {
            response.json().then(data => alert(data.status));
            disableControls(false);
        }
    });
}

function stopAnalysis() {
    disableControls(false);
    fetch('/stop-analysis', { method: 'POST' });
}

function startCalibration() {
    disableControls(true);
    const btn = document.getElementById('calibrateBtn');
    btn.innerText = 'Calibrating...';
    fetch('/calibrate', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert('Calibration completed: ' + data.values);
            btn.innerText = 'Start Calibration';
            disableControls(false);
        })
        .catch(error => {
            alert('Calibration failed: ' + error);
            btn.innerText = 'Start Calibration';
            disableControls(false);
        });
}

function updateSettings() {
    const lowcut = document.getElementById('lowcut').value;
    const highcut = document.getElementById('highcut').value;
    const order = document.getElementById('order').value;
    const gain = document.getElementById('gain').value;
    const baseline_correction_enabled = document.getElementById('baseline_correction_enabled').checked;
    const enabled_channels = document.getElementById('enabled_channels').value;
    const ref_enabled = document.getElementById('ref_enabled').checked;
    const biasout_enabled = document.getElementById('biasout_enabled').checked;
    const bandpass_filter_enabled = document.getElementById('bandpass_filter_enabled').checked;
    const smoothing_enabled = document.getElementById('smoothing_enabled').checked;
    const acquisition_method = document.getElementById('acquisition_method').value;

    document.getElementById('lowcutValue').innerText = lowcut;
    document.getElementById('highcutValue').innerText = highcut;
    document.getElementById('orderValue').innerText = order;
    document.getElementById('enabledChannelsValue').innerText = enabled_channels;

    createChart();

    fetch('/update-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            lowcut,
            highcut,
            order,
            gain,
            baseline_correction_enabled,
            enabled_channels,
            ref_enabled,
            biasout_enabled,
            bandpass_filter_enabled,
            smoothing_enabled,
            acquisition_method
        })
    });

    if (acquisition_method === "brainflow") {
        disableSpiSettings();
    } else {
        enableSpiSettings();
    }
}

function disableControls(disable) {
    document.getElementById('startBtn').disabled = disable;
    document.getElementById('stopBtn').disabled = !disable;
    document.getElementById('calibrateBtn').disabled = disable;
    document.getElementById('exportBtn').disabled = disable;
    document.getElementById('lowcut').disabled = disable;
    document.getElementById('highcut').disabled = disable;
    document.getElementById('order').disabled = disable;
    document.getElementById('gain').disabled = disable;
    document.getElementById('baseline_correction_enabled').disabled = disable;
    document.getElementById('enabled_channels').disabled = disable;
    document.getElementById('ref_enabled').disabled = disable;
    document.getElementById('biasout_enabled').disabled = disable;
    document.getElementById('bandpass_filter_enabled').disabled = disable;
    document.getElementById('smoothing_enabled').disabled = disable;
    document.getElementById('acquisition_method').disabled = disable;
}

function disableSpiSettings() {
    const elements = [
        'lowcut', 'highcut', 'order', 'gain', 'enabled_channels',
        'ref_enabled', 'biasout_enabled', 
        'smoothing_enabled'
    ];
    elements.forEach(id => document.getElementById(id).disabled = true);
}

function enableSpiSettings() {
    const elements = [
        'lowcut', 'highcut', 'order', 'gain', 
        'enabled_channels', 'ref_enabled', 'biasout_enabled', 
        'smoothing_enabled'
    ];
    elements.forEach(id => document.getElementById(id).disabled = false);
}

function exportData() {
    const numRows = prompt("Enter the number of rows to export:", 5000);
    fetch(`/export-data?num_rows=${numRows}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'eeg_data.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(err => console.error('Error exporting data:', err));
}

document.addEventListener("DOMContentLoaded", function () {
    const colorBoxes = document.querySelectorAll('.color-box');
    colorBoxes.forEach(box => {
        box.addEventListener('click', function () {
            const label = this.getAttribute('data-label');
            const dataset = eegChart.data.datasets.find(ds => ds.label === label);
            if (dataset) {
                dataset.hidden = !dataset.hidden;
                eegChart.update();
            }
        });
    });
});

// Experiments functions
let currentExperiment = null;

function loadExperiments() {
    fetch('/get_experiments')
        .then(response => response.json())
        .then(experiments => {
            const select = document.getElementById('experimentSelect');
            experiments.forEach(exp => {
                const option = document.createElement('option');
                option.value = exp;
                option.textContent = exp;
                select.appendChild(option);
            });
        });
}

function openFileDialog(fileTypes) {
    return new Promise((resolve, reject) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = fileTypes.map(type => `.${type[1].split('.')[1]}`).join(',');
        input.onchange = e => {
            if (e.target.files.length > 0) {
                resolve(e.target.files[0]);
            } else {
                reject(new Error('No file selected'));
            }
        };
        input.click();
    });
}

function displayPlot(plotData, plotTitle, stats) {
    console.log('displayPlot function called');
    const popup = document.getElementById('plotPopup');
    const plotImage = document.getElementById('plotImage');
    const plotTitleElement = document.getElementById('plotTitle');
    const plotStats = document.getElementById('plotStats');

    plotImage.src = `data:image/png;base64,${plotData}`;
    plotTitleElement.textContent = plotTitle;

    if (stats) {
        let statsObj = JSON.parse(stats);
        let statsHTML = '<table><tr><th>Channel</th><th>Min</th><th>Max</th><th>Mean</th><th>Std</th></tr>';
        for (const [channel, values] of Object.entries(statsObj)) {
            statsHTML += `<tr><td>${channel}</td><td>${values.min.toFixed(2)}</td><td>${values.max.toFixed(2)}</td><td>${values.mean.toFixed(2)}</td><td>${values.std.toFixed(2)}</td></tr>`;
        }
        statsHTML += '</table>';
        plotStats.innerHTML = statsHTML;
    } else {
        plotStats.innerHTML = 'No statistics available';
    }

    popup.style.display = 'block';
}

socket.on('experiment_error', function(data) {
    console.error('Experiment error:', data.message);
    document.getElementById('experimentResults').innerHTML += `<p style="color: red;">Error: ${data.message}</p>`;
});

socket.on('file_ready', function(data) {
    console.log('File is ready:', data);
    // You can add any client-side logic here that needs to run when the file is ready
});

let originalBodyOverflow;

// Used to disable the controls of the parent window while plot window is displayed. 
function disableParentControls() {
    originalBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.body.classList.add('popup-active');
    
    // Disable all interactive elements except those in the popup
    const interactiveElements = document.querySelectorAll('button, input, select, textarea, a');
    interactiveElements.forEach(element => {
        if (!element.closest('.popup-content')) {
            element.setAttribute('disabled', 'disabled');
            if (element.tagName === 'A') {
                element.setAttribute('tabindex', '-1');
            }
        }
    });
}

// Used to enable the controls of the parent window while plot window is displayed.
function enableParentControls() {
    document.body.style.overflow = originalBodyOverflow;
    document.body.classList.remove('popup-active');
    
    // Re-enable all interactive elements
    const interactiveElements = document.querySelectorAll('button, input, select, textarea, a');
    interactiveElements.forEach(element => {
        element.removeAttribute('disabled');
        if (element.tagName === 'A') {
            element.removeAttribute('tabindex');
        }
    });
}

//Enroll Brainwaves Functions
function showEnrollBrainwavesPopup() {
    console.log('showEnrollBrainwavesPopup called');
    const popup = document.getElementById('enrollBrainwavesPopup');
    console.log('Popup element:', popup);
    if (popup) {
        fadeIn(popup)
        disableParentControls();
    } else {
        console.error('Enroll Brainwaves popup element not found');
    }
}

function hideEnrollBrainwavesPopup() {
    console.log('hideEnrollBrainwavesPopup called');
    const popup = document.getElementById('enrollBrainwavesPopup');
    console.log('Popup element:', popup);
    if (popup) {
        fadeOut(popup);
        enableParentControls();
    } else {
        console.error('Enroll Brainwaves popup element not found');
    }
}

function showInstruction(text) {
    console.log('Showing instruction:', text);
    const instruction = document.getElementById('enrollBrainwavesInstruction');
    instruction.textContent = text;
    fadeIn(instruction);
}

function hideInstruction() {
    console.log('Hiding enrollBrainwavesInstruction');
    const instruction = document.getElementById('enrollBrainwavesInstruction');
    fadeOut(instruction);
}

function showCheckeredGrid() {
    console.log('Showing checkered grid');
    const grid = document.getElementById('checkeredGrid');
    grid.innerHTML = createCheckeredGrid(10, 10);
    fadeIn(grid);
}

function hideCheckeredGrid() {
    console.log('Hiding checkeredGrid');
    const grid = document.getElementById('checkeredGrid');
    fadeOut(grid);
}

function showBreathingCircle(data) {
    console.log('Showing breathing circle');
    const circle = document.getElementById('breathingCircle');
    circle.innerHTML = createBreathingCircle();
    fadeIn(circle);
    animateBreathingCircle(data.expand_time, data.hold_time, data.shrink_time);
}

function hideBreathingCircle() {
    console.log('Hiding breathingCircle');
    const circle = document.getElementById('breathingCircle');
    fadeOut(circle);
}

function showText(data) {
    console.log('Showing text:', data.text);
    const textDisplay = document.getElementById('textDisplay');
    textDisplay.textContent = data.text;
    fadeIn(textDisplay);
}

function hideText() {
    console.log('Hiding textDisplay');
    const textDisplay = document.getElementById('textDisplay');
    fadeOut(textDisplay);
}

function showProgressBar(data) {
    const progressBar = document.getElementById('enrollBrainwavesProgress');
    const progressElement = progressBar.querySelector('.progress');
    const countdownElement = document.createElement('div');
    countdownElement.className = 'countdown';
    progressBar.appendChild(countdownElement);

    const duration = data.duration;
    const startTime = data.start_time * 1000; // Convert to milliseconds
    
    function updateProgress() {
        const currentTime = Date.now();
        const elapsedTime = (currentTime - startTime) / 1000; // in seconds
        const remainingTime = Math.max(0, duration - elapsedTime);
        const progressPercentage = ((duration - remainingTime) / duration) * 100;

        progressElement.style.width = `${progressPercentage}%`;
        countdownElement.textContent = Math.ceil(remainingTime);

        if (remainingTime > 0) {
            requestAnimationFrame(updateProgress);
        }
    }

    fadeIn(progressBar);
    animateProgressBar(data.duration);
}

function hideProgressBar() {
    const progressBar = document.getElementById('enrollBrainwavesProgress');
    fadeOut(progressBar);
    const countdownElement = progressBar.querySelector('.countdown');
    if (countdownElement) {
        countdownElement.remove();
    }
}

function fetchAndGeneratePlots(sessionId) {
    console.log('Fetching features for session:', sessionId);

    fetch(`/get_features/${sessionId}`)
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);

            if (data.length === 0) {
                console.error('No features found for session:', sessionId);
                return;
            }

            const container = document.getElementById('embeddedPlotsContainer');
            container.innerHTML = '';  // Clear any existing content

            data.forEach(item => {
                const [taskName, encodedFeatures] = item;

                console.log('Processing task:', taskName);
                console.log('Encoded features:', encodedFeatures);

                // Decode the base64-encoded features
                const decodedFeatures = new Float64Array(
                    atob(encodedFeatures).split('').map(char => char.charCodeAt(0))
                );

                console.log('Decoded features:', decodedFeatures);

                // Generate the plot using the decoded features
                const plotData = generatePlotData(decodedFeatures);

                console.log('Generated plot data:', plotData);

                // Create a new div for the plot and title
                const plotDiv = document.createElement('div');
                plotDiv.className = 'plotDiv';

                const plotTitleElement = document.createElement('h3');
                plotTitleElement.textContent = taskName;
                plotDiv.appendChild(plotTitleElement);

                // Create and append the plot image
                const plotCanvas = document.createElement('canvas');
                plotDiv.appendChild(plotCanvas);

                // Append the plot div to the container
                container.appendChild(plotDiv);

                // Render the chart
                new Chart(plotCanvas, plotData);
            });
        })
        .catch(error => console.error('Error fetching features:', error));
}

function generatePlotData(features) {
    console.log('Generating plot data for features:', features);

    // Use Chart.js to generate the plot
    const data = {
        labels: [...Array(features.length).keys()],
        datasets: [{
            label: 'EEG Data',
            data: features,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            tension: 0.1
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'EEG Data Plot'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Sample'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amplitude'
                    }
                }
            }
        }
    };

    return config;
}

function showEmbeddedPlot(sessionId) {
    console.log('showEmbeddedPlot function called');
    fetchAndGeneratePlots(sessionId);
    const container = document.getElementById('embeddedPlotsContainer');
    fadeIn(container);
}

function hideEmbeddedPlot() {
    console.log('Hiding embedded plots');
    const container = document.getElementById('embeddedPlotsContainer');

    fadeOut(container);
}

function fadeIn(element, duration = 1000) {
    console.log('Fading in element:', element);
    element.style.opacity = 0;
    element.style.display = 'block';

    const start = performance.now();

    (function fade() {
        const currentTime = performance.now();
        const elapsed = currentTime - start;

        if (elapsed < duration) {
            element.style.opacity = elapsed / duration;
            //console.log('Fade progress:', element.style.opacity);
            requestAnimationFrame(fade);
        } else {
            element.style.opacity = 1;
            console.log('Fade in complete');
        }
    })();
}

function fadeOut(element, duration = 1000) {
    console.log('Fading out element:', element);
    element.style.opacity = 1;

    const start = performance.now();

    (function fade() {
        const currentTime = performance.now();
        const elapsed = currentTime - start;

        if (elapsed < duration) {
            element.style.opacity = 1 - (elapsed / duration);
            //console.log('Fade progress:', element.style.opacity);
            requestAnimationFrame(fade);
        } else {
            element.style.opacity = 0;
            element.style.display = 'none';
            console.log('Fade out complete');
        }
    })();
}

function createCheckeredGrid(rows, cols) {
    let svg = `<svg viewBox="0 0 ${cols * 10} ${rows * 10}" xmlns="http://www.w3.org/2000/svg">`;
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if ((i + j) % 2 === 0) {
                svg += `<rect x="${j * 10}" y="${i * 10}" width="10" height="10" fill="white" />`;
            }
        }
    }
    svg += '</svg>';
    console.log('Created SVG:', svg);
    return svg;
}

function createBreathingCircle() {
    return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="40" fill="none" stroke="white" stroke-width="2" />
    </svg>`;
}

function animateBreathingCircle(expandTime, holdTime, shrinkTime) {
    const circle = document.querySelector('#breathingCircle circle');
    const animate = () => {
        circle.animate([
            { r: 20 },
            { r: 40 },
            { r: 40 },
            { r: 20 }
        ], {
            duration: (expandTime + holdTime + shrinkTime) * 1000,
            easing: 'ease-in-out'
        });
    };
    animate();
    setInterval(animate, (expandTime + holdTime + shrinkTime) * 1000);
}

function animateProgressBar(duration) {
    const progress = document.querySelector('#enrollBrainwavesProgress .progress');
    progress.style.transition = `width ${duration}s linear`;
    progress.style.width = '100%';
    setTimeout(() => {
        progress.style.width = '0%';
    }, 100);
}

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

socket.on('experiment_update', function(data) {
    console.log('Received experiment update:', data);

    if (data.action === 'start_analysis') {
        console.log('Handling start_analysis action');
        startAnalysis()
    } else if (data.action === 'stop_analysis') {
        console.log('Handling stop_analysis action');
        stopAnalysis()
    } else if (data.action === 'open_file_dialog') {
        console.log('Handling open_file_dialog action');
        openFileDialog(data.fileTypes).then(file => {
            if (file) {
                console.log('File selected:', file.name);
                const reader = new FileReader();
                reader.onload = function(e) {
                    console.log('File read complete, sending data to server');
                    socket.emit('set_file_path', e.target.result);
                };
                reader.onerror = function(e) {
                    console.error('Error reading file:', e);
                    socket.emit('experiment_error', {"message": `Error reading file: ${e}`});
                };
                reader.readAsText(file);
            } else {
                console.error('No file selected');
                socket.emit('experiment_error', {"message": "No file selected"});
            }
        }).catch(error => {
            console.error('Error in file dialog:', error);
            socket.emit('experiment_error', {"message": `Error in file dialog: ${error}`});
        });
    } else if (data.action === 'display_plot') {
        console.log('Handling display_plot action');
        displayPlot(data.plot, data.plotTitle, data.stats);
    } else if (data.action === 'open_popup') {
        console.log('Handling open_popup action');
        showEnrollBrainwavesPopup();
    } else if (data.action === 'close_popup') {
        console.log('Handling close_popup action');
        hideEnrollBrainwavesPopup();
    } else if (data.action === 'show_instruction') {
        console.log('Handling show_instruction action');
        showInstruction(data.message);
    } else if (data.action === 'hide_instruction') {
        console.log('Handling hide_instruction action');
        hideInstruction();
    } else if (data.action === 'show_checkered_grid') {
        console.log('Handling show_checkered_grid action');
        showCheckeredGrid();
    } else if (data.action === 'hide_checkered_grid') {
        console.log('Handling hide_checkered_grid action');
        hideCheckeredGrid();
    } else if (data.action === 'show_breathing_circle') {
        console.log('Handling show_breathing_circle action');
        showBreathingCircle(data.data);
    } else if (data.action === 'hide_breathing_circle') {
        console.log('Handling hide_breathing_circle action');
        hideBreathingCircle();
    } else if (data.action === 'show_text') {
        console.log('Handling show_text action');
        showText(data.data);
    } else if (data.action === 'hide_text') {
        console.log('Handling hide_text action');
        hideText();
    } else if (data.action === 'show_progress_bar') {
        console.log('Handling show_progress_bar action');
        showProgressBar(data.data);
    } else if (data.action === 'hide_progress_bar') {
        console.log('Handling hide_progress_bar action');
        hideProgressBar();
    } else if (data.action === 'show_embedded_plot') {
        console.log('Handling show_embedded_plot action');
        if (data.sessionId) {
            console.log('Showing plots for session ', data.sessionId);
            showEmbeddedPlot(data.sessionId);
        } else {
            console.error('No session ID provided for show_embedded_plot action');
        }
    } else if (data.action === 'hide_embedded_plot') {
        console.log('Handling hide_embedded_plot action');
        hideEmbeddedPlot();
    } else {
        console.log('Unhandled action:', data.action);
    }

    // Display messages in the experiment results area
    if (data.message) {
        const experimentResults = document.getElementById('experimentResults');
        experimentResults.innerHTML += `<p>${data.message}</p>`;
        experimentResults.scrollTop = experimentResults.scrollHeight;
    }
});
