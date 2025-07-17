let BASE = "http://127.0.0.1:5000"; // Local development server

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

  const codes = await res.json();
  if (!Array.isArray(codes)) {
    alert("Error generating DMC codes.");
    return;
  }

  const container = document.getElementById("dmc-container");
  container.innerHTML = ""; // clear previous

  codes.forEach(code => {
    const box = document.createElement("div");
    box.className = "qr-box";
    box.innerHTML = `
      <input type="checkbox" name="codes" value="${code.file}" checked>
      <img src="${BASE}/qrs/${code.file}" alt="DMC" />
      <p style="display:none;">${code.content}</p>
    `;
    container.appendChild(box);
  });

  loadHistory();
}

async function readDMC() {
  const fileInput = document.getElementById("dmc-file-input");
  const resultDiv = document.getElementById("upload-result");
  
  if (!fileInput.files[0]) {
    alert("Please select an image file.");
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  // Show loading message
  resultDiv.style.display = "block";
  resultDiv.className = "result-box";
  resultDiv.innerHTML = "🔄 Reading DMC code...";

  try {
    const res = await fetch(`${BASE}/read_dmc`, {
      method: "POST",
      body: formData
    });

    const result = await res.json();

    if (result.success) {
      resultDiv.className = "result-box success";
      resultDiv.innerHTML = `
        <h4>✅ DMC Code Successfully Read!</h4>
        <p><strong>Decoded Text:</strong> ${result.decoded_text}</p>
        <p><strong>File:</strong> ${result.filename}</p>
        <p><strong>Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
      `;
      
      // Refresh history to show the read operation
      loadHistory();
    } else {
      resultDiv.className = "result-box error";
      resultDiv.innerHTML = `
        <h4>❌ Error</h4>
        <p>${result.error}</p>
      `;
    }
  } catch (error) {
    resultDiv.className = "result-box error";
    resultDiv.innerHTML = `
      <h4>❌ Error</h4>
      <p>Failed to read DMC code: ${error.message}</p>
    `;
  }

  // Clear the file input
  fileInput.value = "";
}

// Camera functionality

function switchReaderTab(tab) {
  // Update tab buttons
  document.getElementById('camera-tab').classList.toggle('active', tab === 'camera');
  document.getElementById('upload-tab').classList.toggle('active', tab === 'upload');
  
  // Show/hide content
  document.getElementById('camera-reader').style.display = tab === 'camera' ? 'block' : 'none';
  document.getElementById('upload-reader').style.display = tab === 'upload' ? 'block' : 'none';
  
  // Stop camera if switching away
  if (tab !== 'camera' && cameraStream) {
    stopCamera();
  }
}

async function startCamera() {
  // Load camera history
  loadCameraHistory();
  
  try {
    const constraints = {
      video: {
        facingMode: 'environment', // Use back camera on mobile
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    };

    cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
    const video = document.getElementById('camera-video');
    video.srcObject = cameraStream;
    
    // Update button visibility
    document.getElementById('start-camera-btn').style.display = 'none';
    document.getElementById('stop-camera-btn').style.display = 'inline-block';
    document.getElementById('capture-btn').style.display = 'inline-block';
    
    // Start continuous scanning
    startContinuousScanning();
    
  } catch (error) {
    console.error('Error accessing camera:', error);
    alert('Unable to access camera. Please check permissions or try uploading an image instead.');
  }
}

function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  
  isScanning = false;
  
  // Reset video
  const video = document.getElementById('camera-video');
  video.srcObject = null;
  
  // Update button visibility
  document.getElementById('start-camera-btn').style.display = 'inline-block';
  document.getElementById('stop-camera-btn').style.display = 'none';
  document.getElementById('capture-btn').style.display = 'none';
  
  // Clear results
  document.getElementById('camera-result').style.display = 'none';
}

function startContinuousScanning() {
  isScanning = true;
  updateScanningStatus("🔍 Scanning for DMC codes...", "scanning");
  
  function scan() {
    if (!isScanning || !cameraStream) return;
    
    // Auto-capture every 1.5 seconds for better responsiveness
    setTimeout(() => {
      if (isScanning) {
        captureImage(true); // silent capture
        scan(); // Continue scanning
      }
    }, 1500);
  }
  
  scan();
}

function updateScanningStatus(message, status) {
  const overlay = document.getElementById('camera-overlay');
  const statusElement = overlay.querySelector('.scan-status') || document.createElement('div');
  
  if (!overlay.querySelector('.scan-status')) {
    statusElement.className = 'scan-status';
    overlay.appendChild(statusElement);
  }
  
  statusElement.textContent = message;
  statusElement.className = `scan-status ${status}`;
}

async function captureImage(silent = false) {
  const video = document.getElementById('camera-video');
  const canvas = document.getElementById('camera-canvas');
  const resultDiv = document.getElementById('camera-result');
  
  if (!video.videoWidth || !video.videoHeight) {
    if (!silent) alert('Camera not ready. Please wait a moment.');
    return;
  }
  
  // Set canvas size to match video
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  // Draw current video frame to canvas
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);
  
  // Convert canvas to base64
  const imageData = canvas.toDataURL('image/png');
  
  if (!silent) {
    updateScanningStatus("📸 Capturing image...", "capturing");
    resultDiv.style.display = "block";
    resultDiv.className = "result-box";
    resultDiv.innerHTML = "🔄 Scanning for DMC code...";
  }

  try {
    const res = await fetch(`${BASE}/read_dmc_camera`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const result = await res.json();

    if (result.success) {
      // DETECTION POINT - STOP SCANNING AND CAMERA
      isScanning = false;
      
      // Stop camera stream
      stopCamera();
      
      // Add to camera history
      addToCameraHistory(result);
      
      // Update visual feedback
      const scanFrame = document.querySelector('.scan-frame');
      scanFrame.style.borderColor = '#34c759';
      scanFrame.style.boxShadow = '0 0 0 2000px rgba(52, 199, 89, 0.3)';
      
      updateScanningStatus("✅ DMC Code Detected!", "success");
      
      // Show detailed results
      resultDiv.className = "result-box success";
      resultDiv.innerHTML = `
        <div class="detection-success">
          <h4>🎯 DMC CODE DETECTED!</h4>
          <div class="detected-code">
            <p class="code-value">${result.decoded_text}</p>
          </div>
          <div class="detection-details">
            <p><strong>📷 Source:</strong> Live Camera Scan</p>
            <p><strong>⏰ Detected at:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
            <p><strong>🔍 Scan Duration:</strong> ${(Date.now() - scanStartTime) / 1000}s</p>
          </div>
          <div class="detection-actions">
            <button onclick="startNewScan()" class="resume-btn">🔄 Scan Another Code</button>
            <button onclick="copyToClipboard('${result.decoded_text}')" class="copy-btn">📋 Copy Code</button>
            <button onclick="showCameraHistory()" class="history-btn">📚 View History</button>
          </div>
        </div>
      `;
      
      // Play success sound (if supported)
      playDetectionSound();
      
      // Add visual pulse effect
      addDetectionPulse();
      
      // Refresh history
      loadHistory();
      
      // Update button states
      document.getElementById('start-camera-btn').textContent = '� Start Camera';
      document.getElementById('capture-btn').style.display = 'none';
      
    } else {
      if (!silent) {
        updateScanningStatus("❌ No code found", "error");
        resultDiv.className = "result-box error";
        resultDiv.innerHTML = `
          <h4>❌ No DMC Code Found</h4>
          <p>Position the DMC code within the scanning frame and try again.</p>
          <button onclick="captureImage()" class="retry-btn">🔄 Try Again</button>
        `;
      } else {
        // Continue scanning silently
        updateScanningStatus("🔍 Scanning for DMC codes...", "scanning");
      }
    }
  } catch (error) {
    isScanning = false;
    updateScanningStatus("💥 Scan error", "error");
    if (!silent) {
      resultDiv.className = "result-box error";
      resultDiv.innerHTML = `
        <h4>❌ Scanning Error</h4>
        <p>Failed to scan: ${error.message}</p>
        <button onclick="resumeScanning()" class="retry-btn">🔄 Try Again</button>
      `;
    }
  }
}

// Helper functions for detection point

function addToCameraHistory(result) {
  const historyItem = {
    code: result.decoded_text,
    timestamp: result.timestamp,
    scanDuration: (Date.now() - scanStartTime) / 1000,
    source: 'Live Camera'
  };
  
  // Add to beginning of array
  cameraHistory.unshift(historyItem);
  
  // Keep only last 10 scans
  if (cameraHistory.length > 10) {
    cameraHistory = cameraHistory.slice(0, 10);
  }
  
  // Save to localStorage
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
    alert('No camera scan history available.');
    return;
  }
  
  const historyHtml = cameraHistory.map((item, index) => `
    <div class="history-item">
      <div class="history-header">
        <span class="history-number">#${index + 1}</span>
        <span class="history-source">📷 ${item.source}</span>
      </div>
      <div class="history-code">${item.code}</div>
      <div class="history-details">
        <span>⏰ ${new Date(item.timestamp).toLocaleString()}</span>
        <span>🔍 ${item.scanDuration}s</span>
      </div>
    </div>
  `).join('');
  
  const resultDiv = document.getElementById('camera-result');
  resultDiv.className = "result-box history";
  resultDiv.innerHTML = `
    <div class="camera-history">
      <h4>📚 Camera Scan History (Last 10)</h4>
      <div class="history-list">
        ${historyHtml}
      </div>
      <div class="history-actions">
        <button onclick="startNewScan()" class="resume-btn">🔄 Start New Scan</button>
        <button onclick="clearCameraHistory()" class="clear-btn">🗑️ Clear History</button>
      </div>
    </div>
  `;
}

function clearCameraHistory() {
  if (confirm('Are you sure you want to clear all camera scan history?')) {
    cameraHistory = [];
    localStorage.removeItem('volvo_camera_history');
    showCameraHistory(); // Refresh the display
  }
}

function startNewScan() {
  // Clear results
  document.getElementById('camera-result').style.display = 'none';
  
  // Reset timer
  scanStartTime = Date.now();
  
  // Start camera again
  startCamera();
}

function stopCamera() {
  if (cameraStream) {
    // Stop all tracks
    cameraStream.getTracks().forEach(track => {
      track.stop();
    });
    cameraStream = null;
  }
  
  // Clear video element
  const video = document.getElementById('camera-video');
  if (video) {
    video.srcObject = null;
  }
  
  // Update UI
  document.getElementById('start-camera-btn').textContent = '📱 Start Camera';
  document.getElementById('capture-btn').style.display = 'none';
  
  // Clear overlay status
  const overlay = document.getElementById('camera-overlay');
  const statusElement = overlay.querySelector('.scan-status');
  if (statusElement) {
    statusElement.remove();
  }
}

function resumeScanning() {
  if (!cameraStream) {
    alert('Camera not available. Please start the camera first.');
    return;
  }
  
  // Reset visual elements
  const scanFrame = document.querySelector('.scan-frame');
  scanFrame.style.borderColor = '#007aff';
  scanFrame.style.boxShadow = '0 0 0 2000px rgba(0, 0, 0, 0.5)';
  
  // Reset timer
  scanStartTime = Date.now();
  
  // Update button
  document.getElementById('capture-btn').textContent = '📸 Scan Code';
  
  // Clear results
  document.getElementById('camera-result').style.display = 'none';
  
  // Resume scanning
  startContinuousScanning();
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Show temporary feedback
    const copyBtn = document.querySelector('.copy-btn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = '✅ Copied!';
    copyBtn.style.backgroundColor = '#34c759';
    
    setTimeout(() => {
      copyBtn.textContent = originalText;
      copyBtn.style.backgroundColor = '';
    }, 2000);
  }).catch(() => {
    alert('Failed to copy to clipboard');
  });
}

function playDetectionSound() {
  try {
    // Create a simple success beep
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

function addDetectionPulse() {
  const scanFrame = document.querySelector('.scan-frame');
  scanFrame.style.animation = 'detectionPulse 1s ease-in-out';
  
  setTimeout(() => {
    scanFrame.style.animation = '';
  }, 1000);
}



let allSelected = true;
function toggleSelectAll() {
  const boxes = document.querySelectorAll('input[name="codes"]');
  boxes.forEach(cb => cb.checked = allSelected);
  allSelected = !allSelected;
}

function deleteSelected() {
  const selected = document.querySelectorAll('input[name="codes"]:checked');
  selected.forEach(cb => cb.closest(".qr-box").remove());
}

function getSelectedCodes() {
  const boxes = document.querySelectorAll('input[name="codes"]:checked');
  return Array.from(boxes).map(cb => cb.value);
}

function postExportRequest(endpoint, selectedFiles) {
  fetch(`${BASE}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ files: selectedFiles })
  })
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      const ts = new Date().toISOString().replace(/[:.]/g, "-");
      const ext = endpoint.includes("pdf") ? "pdf" : "xlsx";
      a.href = url;
      a.download = `DMC_Export_${ts}.${ext}`;
      a.click();
    });
}

function downloadPDF() {
  const selected = getSelectedCodes();
  if (selected.length === 0) return alert("Select at least one code.");
  postExportRequest("/download_pdf", selected);
}

function downloadExcel() {
  const selected = getSelectedCodes();
  if (selected.length === 0) return alert("Select at least one code.");
  postExportRequest("/download_excel", selected);
}

async function loadHistory() {
  const res = await fetch(`${BASE}/history`);
  const data = await res.json();
  let html = "";
  data.reverse().forEach(log => {
    const isReadOperation = log.operation === "read" || log.operation === "camera_read";
    const isCameraRead = log.operation === "camera_read";
    const icon = isCameraRead ? "📷" : isReadOperation ? "📖" : "🏭";
    const operationType = isCameraRead ? "CAMERA SCAN" : isReadOperation ? "FILE READ" : "GENERATED";
    
    html += `
      <div class="history-box">
        <p>${icon} ${operationType}: ${log.content}</p>
        ${!isReadOperation ? `<img src="${BASE}/qrs/${log.file}" width="80" />` : ''}
        ${isReadOperation ? `<p><small>Source: ${log.filename}</small></p>` : ''}
        <p><small>${log.timestamp}</small></p>
      </div>`;
  });
  const history = document.getElementById("history");
  if (history) history.innerHTML = html;
}

// ✅ Hide rest and print only QR codes
window.onbeforeprint = () => {
  document.body.innerHTML = document.getElementById("dmc-container").outerHTML;
};

// ✅ Return to home screen if print is canceled
window.onafterprint = () => {
  location.reload();  // reloads and returns to main screen
};
