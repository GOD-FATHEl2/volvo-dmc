let BASE = ""; // Automatically resolves to current domain
fetch(`/login`)

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
    html += `
      <div class="history-box">
        <p>${log.content}</p>
        <img src="${BASE}/qrs/${log.file}" width="80" />
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
