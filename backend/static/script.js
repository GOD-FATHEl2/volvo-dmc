let BASE = "http://127.0.0.1:5000"; // Local development server
let cameraStream = null;
let isScanning = false;
let scanStartTime = Date.now();
let cameraHistory = []; // Store last 10 camera scans

// Top navbar functions
function toggleDropdown() {
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    if (dropdown && dropdownContent) {
        dropdown.classList.toggle('active');
        dropdownContent.classList.toggle('show');
    }
}

function showNavbarMenu() {
    const navbar = document.getElementById('topNavbar');
    const navbarMenu = document.querySelector('.navbar-menu');
    
    if (navbar && navbarMenu) {
        navbar.style.display = 'flex';
        navbarMenu.style.display = 'flex';
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    if (dropdown && dropdownContent && !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
        dropdownContent.classList.remove('show');
    }
});

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  console.log("Attempting login with:", username, password);
  console.log("BASE URL:", BASE);

  try {
    const res = await fetch(`${BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    console.log("Response status:", res.status);
    console.log("Response ok:", res.ok);

    if (res.ok) {
      console.log("Login successful!");
      document.getElementById("login-screen").style.display = "none";
      document.getElementById("main-screen").style.display = "block";
      loadHistory();
    } else {
      console.log("Login failed with status:", res.status);
      alert("Login failed.");
    }
  } catch (error) {
    console.error("Error during login:", error);
    alert("Network error. Please check if the server is running.");
  }
}

async function generateQR() {
  const prefix = document.getElementById("prefix-dropdown").value;
  if (!prefix) {
    alert("Please select a letter or number.");
    return;
  }

  const form = new FormData();
  form.append("prefix", prefix);
  form.append("count", 30); // fixed to 30

  const res = await fetch(`${BASE}/generate`, {
    method: "POST",
    body: form
  });

  if (res.ok) {
    const data = await res.json();
    displayQRCodes(data.codes);
    loadHistory();
    showNavbarMenu(); // Show navbar menu after generation
  } else {
    alert("Error generating QR codes.");
  }
}

function displayQRCodes(codes) {
  const container = document.getElementById("dmc-container");
  container.innerHTML = "";
  
  codes.forEach(code => {
    const box = document.createElement("div");
    box.className = "qr-box";
    box.innerHTML = `
      <img src="data:image/png;base64,${code.base64}" alt="DMC Code" />
      <p><strong>${code.text}</strong></p>
      <input type="checkbox" onchange="toggleSelection(this, '${code.text}')" />
    `;
    container.appendChild(box);
  });
}

function toggleSelection(checkbox, codeText) {
  // Implementation for selection toggle
}

async function loadHistory() {
  try {
    const res = await fetch(`${BASE}/history`);
    if (res.ok) {
      const data = await res.json();
      console.log("History loaded:", data);
    }
  } catch (error) {
    console.error("Error loading history:", error);
  }
}

async function downloadPDF() {
  try {
    const res = await fetch(`${BASE}/export_pdf`, { method: "POST" });
    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "dmc_codes.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    }
  } catch (error) {
    alert("Error downloading PDF: " + error.message);
  }
}

async function downloadExcel() {
  try {
    const res = await fetch(`${BASE}/export_excel`, { method: "POST" });
    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "dmc_codes.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    }
  } catch (error) {
    alert("Error downloading Excel: " + error.message);
  }
}

function deleteSelected() {
  // Implementation for deleting selected codes
}

// Read DMC Functions
function openReadDMC() {
  document.getElementById('read-dmc-section').style.display = 'block';
  document.getElementById('file-upload-section').style.display = 'none';
}

function closeReadDMC() {
  document.getElementById('read-dmc-section').style.display = 'none';
  document.getElementById('file-upload-section').style.display = 'none';
}

function showFileUpload() {
  document.getElementById('file-upload-section').style.display = 'block';
}

async function readDMCFromFile() {
  const fileInput = document.getElementById('file-input');
  const resultDiv = document.getElementById('file-result');
  
  if (!fileInput.files || !fileInput.files[0]) {
    alert('Please select a file first.');
    return;
  }
  
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);
  
  resultDiv.style.display = "block";
  resultDiv.className = "result-container";
  resultDiv.innerHTML = "🔄 Reading DMC code...";
  
  try {
    const res = await fetch(`${BASE}/read_dmc`, {
      method: "POST",
      body: formData
    });
    
    const result = await res.json();
    
    if (result.success) {
      resultDiv.className = "result-container success";
      resultDiv.innerHTML = `
        <h4>✅ DMC Code Found!</h4>
        <p><strong>Decoded Text:</strong> ${result.decoded_text}</p>
        <p><strong>Source:</strong> File Upload</p>
        <p><strong>Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
      `;
      loadHistory();
    } else {
      resultDiv.className = "result-container error";
      resultDiv.innerHTML = `
        <h4>❌ No DMC Code Found</h4>
        <p>Could not find a valid DMC code in the uploaded image.</p>
      `;
    }
  } catch (error) {
    resultDiv.className = "result-container error";
    resultDiv.innerHTML = `
      <h4>❌ Error</h4>
      <p>Failed to read DMC: ${error.message}</p>
    `;
  }
}

// Floating Camera Scanner Functions
function openCameraScanner() {
  const overlay = document.getElementById('camera-scanner-overlay');
  overlay.style.display = 'flex';
  
  // Load camera history
  loadCameraHistory();
  
  // Start camera after a brief delay to ensure the overlay is visible
  setTimeout(() => {
    startScannerCamera();
  }, 300);
}

function closeScanner() {
  stopScannerCamera();
  document.getElementById('camera-scanner-overlay').style.display = 'none';
  document.getElementById('scanner-result').style.display = 'none';
}

function stopScanner() {
  isScanning = false;
  stopScannerCamera();
  updateScannerStatus("⏸️ Scanner stopped", "stopped");
  
  // Show restart option
  const resultDiv = document.getElementById('scanner-result');
  resultDiv.style.display = 'block';
  resultDiv.className = 'scanner-result';
  resultDiv.innerHTML = `
    <h4>⏸️ Scanner Stopped</h4>
    <p>Camera scanning has been paused.</p>
    <div class="result-actions">
      <button onclick="startScannerCamera()" class="action-btn scan-again-btn">📱 Restart Scanner</button>
    </div>
  `;
}

async function startScannerCamera() {
  const video = document.getElementById('scanner-video');
  const statusDiv = document.getElementById('scanner-status');
  
  updateScannerStatus("📱 Starting camera...", "starting");
  
  try {
    // Stop any existing stream first
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
    
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { 
        facingMode: 'environment',
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    });
    
    video.srcObject = cameraStream;
    
    // Wait for video to be ready
    video.onloadedmetadata = () => {
      updateScannerStatus("🔍 Scanning for DMC codes...", "scanning");
      scanStartTime = Date.now();
      isScanning = true;
      startContinuousScanning();
    };
    
  } catch (error) {
    console.error('Camera error:', error);
    updateScannerStatus("❌ Camera access denied", "error");
    
    const resultDiv = document.getElementById('scanner-result');
    resultDiv.style.display = 'block';
    resultDiv.className = 'scanner-result error';
    resultDiv.innerHTML = `
      <h4>❌ Camera Error</h4>
      <p>Unable to access camera: ${error.message}</p>
      <p>Please ensure camera permissions are granted.</p>
      <div class="result-actions">
        <button onclick="startScannerCamera()" class="action-btn scan-again-btn">🔄 Try Again</button>
      </div>
    `;
  }
}

function stopScannerCamera() {
  isScanning = false;
  
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => {
      track.stop();
    });
    cameraStream = null;
  }
  
  const video = document.getElementById('scanner-video');
  if (video) {
    video.srcObject = null;
  }
}

function startContinuousScanning() {
  if (!isScanning || !cameraStream) return;
  
  // Capture and scan every 1.5 seconds
  setTimeout(() => {
    if (isScanning) {
      captureScannerImage();
      startContinuousScanning(); // Continue scanning
    }
  }, 1500);
}

async function captureScannerImage() {
  if (!isScanning || !cameraStream) return;
  
  const video = document.getElementById('scanner-video');
  const canvas = document.getElementById('scanner-canvas');
  
  if (!video.videoWidth || !video.videoHeight) {
    return; // Video not ready
  }
  
  // Set canvas size to match video
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  // Draw current video frame to canvas
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  
  // Convert canvas to base64
  const imageData = canvas.toDataURL('image/png');
  
  try {
    const res = await fetch(`${BASE}/read_dmc_camera`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const result = await res.json();

    if (result.success) {
      // DETECTION POINT - STOP SCANNING AND SHOW RESULTS
      isScanning = false;
      stopScannerCamera();
      
      // Add to history
      addToCameraHistory(result);
      
      // Update visual feedback
      const scanFrame = document.querySelector('.scanner-overlay-frame .scan-frame');
      if (scanFrame) {
        scanFrame.style.borderColor = '#34c759';
        scanFrame.style.boxShadow = '0 0 0 2000px rgba(52, 199, 89, 0.3)';
      }
      
      updateScannerStatus("✅ DMC Code Detected!", "success");
      
      // Show results
      const resultDiv = document.getElementById('scanner-result');
      resultDiv.style.display = 'block';
      resultDiv.className = 'scanner-result success';
      resultDiv.innerHTML = `
        <h4>🎯 DMC CODE DETECTED!</h4>
        <div class="detected-code">
          <p class="code-value">${result.decoded_text}</p>
        </div>
        <p><strong>📷 Source:</strong> Live Camera Scan</p>
        <p><strong>⏰ Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
        <p><strong>🔍 Duration:</strong> ${(Date.now() - scanStartTime) / 1000}s</p>
        <div class="result-actions">
          <button onclick="startScannerCamera()" class="action-btn scan-again-btn">🔄 Scan Again</button>
          <button onclick="copyToClipboard('${result.decoded_text}')" class="action-btn copy-code-btn">📋 Copy</button>
          <button onclick="showCameraHistory()" class="action-btn history-btn">📚 History</button>
        </div>
      `;
      
      // Play success sound
      playDetectionSound();
      
      // Refresh main history
      loadHistory();
    }
  } catch (error) {
    console.error('Scan error:', error);
    // Continue scanning on error (silent fail for network issues)
  }
}

function updateScannerStatus(message, status) {
  const statusElement = document.getElementById('scanner-status');
  if (statusElement) {
    statusElement.textContent = message;
    statusElement.className = `scanner-status ${status}`;
  }
}

// Camera History Functions
function addToCameraHistory(result) {
  const historyItem = {
    code: result.decoded_text,
    timestamp: result.timestamp,
    scanDuration: (Date.now() - scanStartTime) / 1000,
    source: 'Live Camera'
  };
  
  cameraHistory.unshift(historyItem);
  
  if (cameraHistory.length > 10) {
    cameraHistory = cameraHistory.slice(0, 10);
  }
  
  localStorage.setItem('volvo_camera_history', JSON.stringify(cameraHistory));
}

function loadCameraHistory() {
  try {
    const saved = localStorage.getItem('volvo_camera_history');
    if (saved) {
      cameraHistory = JSON.parse(saved);
    }
  } catch (error) {
    console.log('Could not load camera history:', error);
    cameraHistory = [];
  }
}

function showCameraHistory() {
  loadCameraHistory();
  
  if (cameraHistory.length === 0) {
    const resultDiv = document.getElementById('scanner-result');
    resultDiv.style.display = 'block';
    resultDiv.className = 'scanner-result';
    resultDiv.innerHTML = `
      <h4>📚 Camera History</h4>
      <p>No camera scan history available.</p>
      <div class="result-actions">
        <button onclick="startScannerCamera()" class="action-btn scan-again-btn">🔄 Start Scanning</button>
      </div>
    `;
    return;
  }
  
  const historyHtml = cameraHistory.map((item, index) => `
    <div class="history-item" style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.5rem; margin: 0.5rem 0; text-align: left;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="background: #8e44ad; color: white; padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.7rem;">#${index + 1}</span>
        <span style="color: #666; font-size: 0.8rem;">📷 ${item.source}</span>
      </div>
      <div style="font-family: monospace; font-weight: bold; color: #1d4ed8; word-break: break-all; font-size: 0.9rem; margin: 0.5rem 0; padding: 0.3rem; background: #f0f9ff; border-radius: 4px;">${item.code}</div>
      <div style="display: flex; justify-content: space-between; color: #666; font-size: 0.7rem;">
        <span>⏰ ${new Date(item.timestamp).toLocaleString()}</span>
        <span>🔍 ${item.scanDuration}s</span>
      </div>
    </div>
  `).join('');
  
  const resultDiv = document.getElementById('scanner-result');
  resultDiv.style.display = 'block';
  resultDiv.className = 'scanner-result';
  resultDiv.innerHTML = `
    <h4>📚 Camera History (Last 10)</h4>
    <div style="max-height: 200px; overflow-y: auto;">
      ${historyHtml}
    </div>
    <div class="result-actions">
      <button onclick="startScannerCamera()" class="action-btn scan-again-btn">🔄 New Scan</button>
      <button onclick="clearCameraHistory()" class="action-btn" style="background: #e74c3c;">🗑️ Clear</button>
    </div>
  `;
}

function clearCameraHistory() {
  if (confirm('Clear all camera scan history?')) {
    cameraHistory = [];
    localStorage.removeItem('volvo_camera_history');
    showCameraHistory();
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    updateScannerStatus("📋 Copied to clipboard!", "success");
    setTimeout(() => {
      updateScannerStatus("✅ DMC Code Detected!", "success");
    }, 2000);
  }).catch(() => {
    alert('Failed to copy to clipboard');
  });
}

function playDetectionSound() {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  } catch (error) {
    // Silent fail if audio not supported
  }
}
