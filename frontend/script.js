let BASE = "http://127.0.0.1:5000"; // Local development server

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (res.ok) {
    document.getElementById("login-screen").style.display = "none";
    document.getElementById("main-screen").style.display = "block";
    loadHistory();
  } else {
    alert("Login failed.");
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
  } else {
    alert("Error generating DMC codes.");
  }
}

function displayQRCodes(codes) {
  const container = document.getElementById("dmc-container");
  container.innerHTML = ""; // clear previous

  codes.forEach(code => {
    const box = document.createElement("div");
    box.className = "qr-box";
    box.innerHTML = `
      <input type="checkbox" name="codes" value="${code.text}" checked>
      <img src="data:image/png;base64,${code.base64}" alt="DMC Code" />
      <p><strong>${code.text}</strong></p>
    `;
    container.appendChild(box);
  });
}

async function readDMC() {
  const fileInput = document.getElementById("dmc-file-input");
  const resultDiv = document.getElementById("read-result");
  
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
    const isReadOperation = log.operation === "read";
    const icon = isReadOperation ? "📖" : "🏭";
    const operationType = isReadOperation ? "READ" : "GENERATED";
    
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
