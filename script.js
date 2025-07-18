// VOLVO DMC Generator - Static Web App Edition
// API Configuration
const API_BASE_URL = window.location.origin;

// Global state
let batchResults = [];
let currentStream = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAPIStatus();
});

function initializeApp() {
    updateStatus('ready', 'Ready');
    console.log('VOLVO DMC Generator - Static Web App Edition initialized');
}

function setupEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            switchTab(tabName);
        });
    });

    // Single DMC generation
    document.getElementById('generate-btn').addEventListener('click', generateSingleDMC);
    document.getElementById('dmc-data').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generateSingleDMC();
        }
    });

    // Batch generation
    document.getElementById('generate-batch-btn').addEventListener('click', generateBatchDMC);
    document.getElementById('export-excel-btn').addEventListener('click', () => exportBatch('excel'));
    document.getElementById('export-csv-btn').addEventListener('click', () => exportBatch('csv'));
    document.getElementById('clear-batch-btn').addEventListener('click', clearBatch);

    // Camera controls
    document.getElementById('start-camera-btn').addEventListener('click', startCamera);
    document.getElementById('stop-camera-btn').addEventListener('click', stopCamera);
}

function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-dmc`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: 'test' })
        });
        
        if (response.ok) {
            updateStatus('ready', 'API Ready');
        } else {
            updateStatus('warning', 'API Limited');
        }
    } catch (error) {
        updateStatus('error', 'API Offline');
        console.warn('API not available, using demo mode');
    }
}

async function generateSingleDMC() {
    const data = document.getElementById('dmc-data').value.trim();
    
    if (!data) {
        showAlert('Please enter DMC data', 'warning');
        return;
    }

    showLoading(true);
    updateStatus('processing', 'Generating...');

    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-dmc`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: data })
        });

        const result = await response.json();

        if (result.success) {
            displaySingleDMC(result);
            updateStatus('ready', 'DMC Generated');
        } else {
            throw new Error(result.error || 'Generation failed');
        }
    } catch (error) {
        console.error('Error generating DMC:', error);
        // Fallback to demo mode
        displaySingleDMC({
            success: true,
            image: generateDemoImage(data),
            data: data
        });
        updateStatus('warning', 'Demo Mode');
    } finally {
        showLoading(false);
    }
}

async function generateBatchDMC() {
    const batchData = document.getElementById('batch-data').value.trim();
    
    if (!batchData) {
        showAlert('Please enter batch data', 'warning');
        return;
    }

    const dataLines = batchData.split('\n').filter(line => line.trim());
    
    if (dataLines.length === 0) {
        showAlert('Please enter valid batch data', 'warning');
        return;
    }

    showLoading(true);
    updateStatus('processing', `Generating ${dataLines.length} DMCs...`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-dmc`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ batch_data: dataLines })
        });

        const result = await response.json();

        if (result.success) {
            batchResults = result.batch_results;
            displayBatchResults(batchResults);
            updateStatus('ready', `${batchResults.length} DMCs Generated`);
        } else {
            throw new Error(result.error || 'Batch generation failed');
        }
    } catch (error) {
        console.error('Error generating batch DMCs:', error);
        // Fallback to demo mode
        batchResults = dataLines.map(data => ({
            data: data,
            image: generateDemoImage(data)
        }));
        displayBatchResults(batchResults);
        updateStatus('warning', 'Demo Mode');
    } finally {
        showLoading(false);
    }
}

function displaySingleDMC(result) {
    const resultContainer = document.getElementById('dmc-result');
    resultContainer.innerHTML = `
        <div class="dmc-display">
            <div class="dmc-image">
                <img src="data:image/png;base64,${result.image}" alt="DMC" />
            </div>
            <div class="dmc-info">
                <h4>DMC Data:</h4>
                <p class="dmc-data">${result.data}</p>
                <div class="dmc-actions">
                    <button onclick="downloadImage('${result.image}', '${result.data}')" class="btn secondary">
                        💾 Download Image
                    </button>
                    <button onclick="copyToClipboard('${result.data}')" class="btn secondary">
                        📋 Copy Data
                    </button>
                </div>
            </div>
        </div>
    `;
}

function displayBatchResults(results) {
    const resultsContainer = document.getElementById('batch-results');
    const controlsContainer = document.getElementById('batch-controls');
    
    resultsContainer.innerHTML = results.map((result, index) => `
        <div class="batch-item">
            <div class="batch-image">
                <img src="data:image/png;base64,${result.image}" alt="DMC ${index + 1}" />
            </div>
            <div class="batch-info">
                <p class="batch-data">${result.data}</p>
                <button onclick="downloadImage('${result.image}', '${result.data}')" class="btn secondary small">
                    💾 Download
                </button>
            </div>
        </div>
    `).join('');
    
    controlsContainer.style.display = 'block';
}

async function exportBatch(format) {
    if (batchResults.length === 0) {
        showAlert('No batch results to export', 'warning');
        return;
    }

    showLoading(true);
    updateStatus('processing', 'Exporting...');

    try {
        const exportData = batchResults.map(result => ({
            'DMC Data': result.data,
            'Generated': new Date().toISOString(),
            'Index': batchResults.indexOf(result) + 1
        }));

        const response = await fetch(`${API_BASE_URL}/api/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                data: exportData, 
                format: format 
            })
        });

        const result = await response.json();

        if (result.success) {
            downloadFile(result.file, result.filename, result.mimetype);
            updateStatus('ready', 'Export Complete');
        } else {
            throw new Error(result.error || 'Export failed');
        }
    } catch (error) {
        console.error('Error exporting:', error);
        // Fallback to CSV export
        exportToCSV(batchResults);
        updateStatus('warning', 'Exported as CSV');
    } finally {
        showLoading(false);
    }
}

function exportToCSV(results) {
    const csvContent = [
        ['DMC Data', 'Generated', 'Index'],
        ...results.map((result, index) => [
            result.data,
            new Date().toISOString(),
            index + 1
        ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `volvo_dmc_export_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

function clearBatch() {
    batchResults = [];
    document.getElementById('batch-results').innerHTML = `
        <div class="placeholder">
            <span class="placeholder-icon">📊</span>
            <p>Batch results will appear here</p>
        </div>
    `;
    document.getElementById('batch-controls').style.display = 'none';
    document.getElementById('batch-data').value = '';
}

// Camera functions (placeholder)
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.getElementById('camera-feed');
        video.srcObject = stream;
        currentStream = stream;
        
        document.getElementById('start-camera-btn').disabled = true;
        document.getElementById('stop-camera-btn').disabled = false;
        
        updateStatus('ready', 'Camera Active');
    } catch (error) {
        console.error('Error accessing camera:', error);
        showAlert('Unable to access camera', 'error');
    }
}

function stopCamera() {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
        document.getElementById('camera-feed').srcObject = null;
        
        document.getElementById('start-camera-btn').disabled = false;
        document.getElementById('stop-camera-btn').disabled = true;
        
        updateStatus('ready', 'Camera Stopped');
    }
}

// Utility functions
function generateDemoImage(data) {
    // Create a simple base64 placeholder image
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    
    // Draw placeholder pattern
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, 200, 200);
    
    ctx.fillStyle = 'black';
    for (let i = 0; i < 200; i += 10) {
        for (let j = 0; j < 200; j += 10) {
            if ((i + j) % 20 === 0) {
                ctx.fillRect(i, j, 5, 5);
            }
        }
    }
    
    ctx.fillStyle = 'black';
    ctx.font = '12px Arial';
    ctx.fillText('DMC', 10, 20);
    ctx.fillText(data.substring(0, 15), 10, 35);
    
    return canvas.toDataURL().split(',')[1];
}

function downloadImage(base64, filename) {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${base64}`;
    link.download = `${filename.replace(/[^a-zA-Z0-9]/g, '_')}_dmc.png`;
    link.click();
}

function downloadFile(base64, filename, mimetype) {
    const link = document.createElement('a');
    link.href = `data:${mimetype};base64,${base64}`;
    link.download = filename;
    link.click();
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard', 'success');
    }).catch(() => {
        showAlert('Failed to copy', 'error');
    });
}

function updateStatus(type, message) {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    statusDot.className = `status-dot ${type}`;
    statusText.textContent = message;
}

function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = show ? 'flex' : 'none';
}

function showAlert(message, type = 'info') {
    // Create a simple alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        background: ${type === 'error' ? '#ff3b30' : type === 'warning' ? '#ff9500' : type === 'success' ? '#30d158' : '#007aff'};
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

function showInfo() {
    document.getElementById('info-modal').style.display = 'block';
}

function showHelp() {
    showAlert('Help: Enter DMC data and click generate. Use batch mode for multiple DMCs.', 'info');
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
};
