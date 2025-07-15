import os
import json
import datetime
import sys
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add the backend directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from generate_qr import generate_dmc_code
except ImportError:
    # Fallback for deployment environments
    def generate_dmc_code(data, filepath):
        print(f"Warning: generate_qr module not available. Would generate DMC for: {data}")
        return filepath

app = Flask(__name__)
CORS(app)

# 🔒 Robust path handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "qrs")
LOG_FILE = os.path.join(BASE_DIR, "database.json")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup folders/files safely
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "admin":
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route("/generate", methods=["POST"])
def generate():
    prefix = request.form.get("prefix", "").strip().upper()
    count = int(request.form.get("count", 30))

    if not prefix or not prefix.isalnum() or len(prefix) != 1:
        return jsonify({"error": "Invalid prefix"}), 400

    now = datetime.datetime.now()
    date_part = f"{now.month:01d}{now.day:01d}{str(now.year)[-1]}"
    time_part = f"{now.hour:01d}{now.second:01d}"
    dmc_value = f"{prefix}{date_part}{time_part}"  # e.g. A7725640

    with open(LOG_FILE, "r+") as f:
        history = json.load(f)
        existing = {entry["content"] for entry in history}
        results = []
        timestamp = now.strftime("%Y%m%d%H%M%S")

        for i in range(count):
            final_dmc = dmc_value + str(i) if dmc_value in existing else dmc_value
            filename = secure_filename(f"dmc_{i}_{timestamp}.png")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            generate_dmc_code(final_dmc, filepath)

            entry = {
                "content": final_dmc,
                "file": filename,
                "timestamp": str(now)
            }
            history.append(entry)
            results.append(entry)

        f.seek(0)
        json.dump(history, f, indent=2)
        f.truncate()

    return jsonify(results)

@app.route("/history")
def history():
    with open(LOG_FILE, "r") as f:
        return jsonify(json.load(f))

@app.route("/qrs/<path:filename>")
def get_qr(filename):
    return send_from_directory("static/qrs", filename)

@app.route("/download_excel", methods=["POST"])
def download_excel():
    from openpyxl import Workbook
    selected_files = request.json.get("files", [])
    with open(LOG_FILE) as f:
        logs = json.load(f)
    selected = [l for l in logs if l["file"] in selected_files]

    wb = Workbook()
    ws = wb.active
    ws.title = "DMC Export"
    row = []

    for i, log in enumerate(selected, 1):
        row.append(log["content"])
        if len(row) == 5:
            ws.append(row)
            row = []
    if row:
        while len(row) < 5:
            row.append("")
        ws.append(row)

    ws.oddFooter.center.text = "VOLVO Cars Torslanda All rights reserved. © 2025 Made By: Nawoar Ekkou"
    file = os.path.join(BASE_DIR, "static", f"Export_{datetime.datetime.now().timestamp()}.xlsx")
    wb.save(file)
    return send_file(file, as_attachment=True)

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    from fpdf import FPDF
    selected_files = request.json.get("files", [])
    with open(LOG_FILE) as f:
        logs = json.load(f)
    selected = [l for l in logs if l["file"] in selected_files]

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "VOLVO DMC Export", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(150)
            self.cell(0, 10, "VOLVO Cars Torslanda All rights reserved. © 2025 Made By: Nawoar Ekkou", 0, 0, "C")

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, log in enumerate(selected):
        if i % 30 == 0:
            pdf.add_page()
        x = 10 + (i % 5) * 38
        y = 20 + ((i // 5) % 6) * 38
        pdf.image(os.path.join(app.config["UPLOAD_FOLDER"], log["file"]), x=x, y=y, w=10, h=10)

    pdf_file = os.path.join(BASE_DIR, "static", f"Export_{datetime.datetime.now().timestamp()}.pdf")
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

